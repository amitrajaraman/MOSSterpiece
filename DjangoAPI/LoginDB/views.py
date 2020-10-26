from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from LoginDB.models import Users
from LoginDB.serializers import UserSerializer

from django.core.files.storage import default_storage

# Create your views here.
@csrf_exempt
def userApi(request,del_name=""):
    if request.method=='GET':
        users = Users.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)

    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        user_data = JSONParser().parse(request)
        user=Users.objects.get(name=user_data['name'])
        user_serializer=UserSerializer(user,data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        user=Users.objects.get(name=del_name)
        user.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

@csrf_exempt
def SaveFile(request):
    file=request.FILES['uploadedFile']
    file_name = default_storage.save(file.name,file)

    return JsonResponse(file_name,safe=False)