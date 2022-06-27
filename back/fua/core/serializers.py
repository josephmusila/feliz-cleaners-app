from dataclasses import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import services
from . import models
from django.conf import settings

class ImageSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    label=serializers.CharField()
    image=serializers.ImageField()

    def get_profile_picture_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(settings.MEDIA_URL + obj['image'])


    def to_internal_value(self, data):
        data=super().to_internal_value(data)
        return services.ImageService(**data)


class UserSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    phone=serializers.CharField()
    email=serializers.EmailField(validators=[
        UniqueValidator(
            queryset=models.User.objects.all(),
            message='A user with such email address already exists'
        )]
    )
    password=serializers.CharField(write_only=True)
    avatar=serializers.ImageField()
    location=serializers.CharField()


    def to_internal_value(self, data):
        data=super().to_internal_value(data)

        return services.UserDataClass(**data)

class CurrentUserSerializer(serializers.ModelSerializer):
    model= models.User

    fields=['id',]


class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=220,write_only=True)

    class Meta:
        model=models.User

        fields=("email","password","token")

        read_only_fields=['token']

# http://192.168.1.101:8000/api/user/ -H 'Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZXhwIjoxNjU1ODE2Nzk4LCJpYXQiOjE2NTU3MzAzOTh9.1KIRe6B0xIRIAaglBzsZyJ-4iH0u2dRD3lc5hepO6GA'