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

# Create your views here.
# @csrf_exempt
# def userApi(request,del_name=""):
#     if request.method=='GET':
#         users = Users.objects.all()
#         user_serializer = UserSerializer(users, many=True)
#         return JsonResponse(user_serializer.data, safe=False)


class userAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_data=JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({
                "user": UserSerializer(user,
                                       context=self.get_serializer_context()).data,
            })
        return JsonResponse("Failed to Add.",safe=False)
    

class fileAPI(generics.GenericAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

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
        return Response({
            "file_name": path_to_file})

class loginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        user_data = JSONParser().parse(request)
        serializer = LoginSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth.login(request, user)
        token, created  = Token.objects.get_or_create(user=user)
        # print(token.key)
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "token": token.key
        })  

class logoutAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        auth.logout(request)
        return Response({})

class changeAPI(generics.UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = User
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
class processAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(os.getcwd())
        #Get the needed file
        req_file = Files.objects.filter(files=request.POST.get('file'))
        path_to_zip = "../DjangoAPI/media/" + str(req_file[0].files)         #to be passed as an argument to Amit's file
        path_to_an = "../backend_LSA/mainback.py"
        os.system("python " + path_to_an + " " + path_to_zip)
        return Response({"does it work": "Yes it does"})