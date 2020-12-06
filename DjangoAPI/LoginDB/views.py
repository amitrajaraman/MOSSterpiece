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

class userAPI(generics.GenericAPIView):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        files = Files(files = request.FILES['file'], username=request.user.username)
        files.save()
        file_name = files.files.name
        # print(file_name)
        return Response({
            "file_name": file_name})

    def get(self, request):
        file_name = request.GET.get('path')
        path_to_file = settings.MEDIA_ROOT + "/" + file_name
        zip_file = open(path_to_file, 'rb')
        response = HttpResponse(zip_file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="download.zip"'
        
        return response

class loginAPI(generics.GenericAPIView):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(os.getcwd())
        #Get the needed file
        req_file = Files.objects.get(files=request.POST.get('file'))
        print(request.POST.get('file'))
        path_to_zip = "../DjangoAPI/media/" + str(req_file.files)         #to be passed as an argument to Amit's file
        path_to_an = "../backend_LSA/mainBack.py"
        os.system("python " + path_to_an + " " + path_to_zip)
        return Response({"does it work": "Yes it does"})
