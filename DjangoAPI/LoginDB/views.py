from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from LoginDB.models import Users, Files
from LoginDB.serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer 
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
import os
import sys
from django.conf import settings
from django.http import HttpResponse, Http404
import shutil
import numpy as np
import scipy.spatial.distance
from zipfile import ZipFile
import subprocess


class userAPI(generics.GenericAPIView):
    """
    UserAPI's post request is used for registering the user.
    Several checks are in place to make sure that the fields aren't repeated twice in the database.
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_data=JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
                "safe": True 
            })
        if User.objects.filter(username=user_serializer.data['username']).exists():
            return Response({
                "message":"Username already exists", 
                "safe":False}
                )
        elif User.objects.filter(email=user_serializer.data['email']).exists():
            return Response({
                "message": "Email already exists",
                "safe":False}
            )
        return Response({
            "message": "Failed to add",
            "safe":False}
        )

class fileAPI(generics.GenericAPIView):
    """
    fileAPI contains requests for download and upload of the zipfiles.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST request saves the name of the uploaded file, hashing it if there's a repetition.
        It is being saved in the db as well, can be used laster to show the previous results.
        """
        files = Files(files = request.FILES['file'], username=request.user.username)
        files.save()
        file_name = files.files.name
        # print(file_name)
        return Response({
            "file_name": file_name})

class loginAPI(generics.GenericAPIView):
    """
    Authenticates the user and logs the person.
    """
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        logged_in = request.user.username
        user_data = JSONParser().parse(request)
        serializer = LoginSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth.login(request, user)
        token, created  = Token.objects.get_or_create(user=user)
        # print(token.key)
        return Response({
            "name": logged_in,
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "token": token.key
        })


class changeAPI(generics.GenericAPIView):
    """
    changeAPI is used for changing the password
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        """
        Check the authentication of the user, and if the passwords match, change the user's password accordingly.
        """
        user = request.user
    
        if not user.check_password(request.data.get("oldpassword")):
            response = {
                'status': 'failure',
                'message': 'Old password does not match',
                'data': []
            }
            return Response(response)
        user.set_password(request.data.get("newpassword"))
        user.save()
        response = {
            'status': 'success',
            'message': 'Password updated successfully',
            'data': []
        }
        return Response(response)

class tokenAPI(generics.GenericAPIView):
    """
    Generates tokens for security reasons
    """
    def get(self, request):
        user = request.user
        token, created = Token.objects.get(user=user)
        print(token.key)
        return Response({"token": token.key})

class logoutAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        auth.logout(request)
        return Response({})

class processAPI(generics.GenericAPIView): 
    """
    processAPI integrates the website with the core logic
    """  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST runs the core logic by passing the data obtained from the frontend as arguments.
        The outputs are stored in a pre-determined folder, which can then be downloaded at the user's pleasure.
        """
        print(os.getcwd())
        #Get the needed file

        req_file = Files.objects.get(files=request.data["file"],username=request.user.username)
        path_to_zip = "../DjangoAPI/media/" + str(req_file.files)         #to be passed as an argument to Amit's file
        path_to_an = "../backend_LSA/mainBack.py"
        try:
            os.system("python3 " + path_to_an + " " + path_to_zip)
        except err:
            print("There was an error while processing")
            return Response({"safe":False})
        name = "results_" + req_file.files.name.split('.')[0]
        print("name is "+ name)
        shutil.make_archive(name, 'zip', "media/results")
        name = name + ".zip"
        if(os.path.exists("media/"+name)):
            os.remove("media/"+name)
        shutil.move(name, "media")
        zip_file = open("media/" + name, 'rb')
        response = HttpResponse(zip_file, content_type='application/x-zip')
        response['Content-Disposition'] = 'attachment; filename={name}'.format(name = name)
        return response
