from logging import exception
from multiprocessing import AuthenticationError
from rest_framework import views,response,exceptions,permissions
from . import serializers as user_serializer
from . import services,authentication
import datetime
import jwt
from rest_framework.generics import ListAPIView
from .serializers import GetUserSerializer
from .models import User
from django.db.models import Q


class GetUser(ListAPIView):
    serializer_class=GetUserSerializer
    queryset=User

    def get_queryset(self):
        #    use self.kwargs ↓
        email_items = self.kwargs.get('email')
        if email_items is not None:
            return User.objects.filter(email=email_items)
        else:
            # return some queryset
            pass

class RegisterApi(views.APIView):

    def post(self,request):
        serializer=user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data=serializer.validated_data
        serializer.instance = services.create_user(user=data)
        print(data)


        # return response.Response(data=serializer.data)
        return response.Response({"message":"Account created Succesfully"})


class LoginAPi(views.APIView):
    def post(self,request):
        email=request.data["email"]
        password=request.data["password"]

        user=services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        token=services.create_token(user_id=user.id)
        resp=response.Response(token)
        resp.set_cookie(key="jwt",value=token,httponly=True)
        return resp


class UserApi(views.APIView):
    authentication_classes=(authentication.CustomUserAuthentication,)
    permission_classes=(permissions.IsAuthenticated,)


    def get(self,request):
        user=request.user

        serializer=user_serializer.UserSerializer(user)

        return response.Response(serializer.data)


class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)

    permission_classes = (permissions.IsAuthenticated,)


    def post(self,request):
        resp=response.Response()
        resp.delete_cookie("jwt")
        resp.data={"message":"so long farewell"}
        return resp