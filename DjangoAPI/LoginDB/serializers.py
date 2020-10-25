from rest_framework import serializers
from LoginDB.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first',
                  'last',
                  'pw',
                  'email',
                  'name')
