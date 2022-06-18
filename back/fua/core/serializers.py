from dataclasses import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import services
from . import models


class UserSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    phone=serializers.CharField()
    email=serializers.EmailField(validators=[
        UniqueValidator(
            queryset=models.User.objects.all(),
            message='Such email address already exists'
        )]
    )
    password=serializers.CharField(write_only=True)


    def to_internal_value(self, data):
        data=super().to_internal_value(data)

        return services.UserDataClass(**data)

class GetUserSerializer(serializers.Serializer):
    class Meta:
        model=models.User
        fields="__all__"