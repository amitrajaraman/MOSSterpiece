from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers, viewsets
import json
from LoginDB.models import Files

class UserSerializer(serializers.ModelSerializer):
    """
    Serializers for storing user's data
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.last_name = validated_data['last_name']
        user.first_name = validated_data['first_name']
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Stored the logged in user's data
    """
    username = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        """
        validate() authenticates the user and is used to check whether the person is valid or not.
        """
        user = authenticate(**data)
        if user is not None:
            return user
        else:
            raise serializers.ValidationError("Incorrect Credentials")


class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for changing the passowords.
    """
    model = User
    oldpassword = serializers.CharField(required=True)
    password = serializers.CharField(required=True)