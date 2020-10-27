from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from LoginDB.models import Users
from LoginDB.serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage

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
            # return JsonResponse("Added Successfully!!" , safe=False)
            token = 12
            return Response({
                "user": UserSerializer(user,
                                       context=self.get_serializer_context()).data,
                "token": token
            })
        return JsonResponse("Failed to Add.",safe=False)
    
    # elif request.method=='PUT':
    #     user_data = JSONParser().parse(request)
    #     user=Users.objects.get(name=user_data['name'])
    #     user_serializer=UserSerializer(user,data=user_data)
    #     if user_serializer.is_valid():
    #         user_serializer.save()
    #         return JsonResponse("Updated Successfully!!", safe=False)
    #     return JsonResponse("Failed to Update.", safe=False)

    # elif request.method=='DELETE':
    #     user=Users.objects.get(name=del_name)
    #     user.delete()
    #     return JsonResponse("Deleted Succeffully!!", safe=False)

@csrf_exempt
def SaveFile(request):
    file=request.FILES['uploadedFile']
    file_name = default_storage.save(file.name,file)

    return JsonResponse(file_name,safe=False)


class loginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user_data = JSONParser().parse(request)
        serializer = LoginSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # auth.login(request, user)
        token,  = Token.objects.get_or_create(user=user)
        # print(token.key)
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "token": token.key
        })  

