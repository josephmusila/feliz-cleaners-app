from distutils.log import INFO
from logging import exception
from multiprocessing import AuthenticationError
from urllib.request import HTTPBasicAuthHandler
from django.http import HttpResponse
from rest_framework import views,response,exceptions,permissions
from . import serializers as user_serializer
from . import services,authentication
import datetime
import jwt
from rest_framework.generics import ListAPIView
# from .serializers import GetUserSerializer
from .models import ImagesForSlide, MpesaPayment, User
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
import requests
import json
from requests.auth import HTTPBasicAuth
from .mpesaCred import  MpesaAccessToken, LipanaMpesaPpassword
from django.http import HttpResponse, JsonResponse
# class GetUser(ListAPIView):
#     serializer_class=GetUserSerializer
#     queryset=User

#     def get_queryset(self):
#         #    use self.kwargs ↓
#         email_items = self.kwargs.get('email')
#         if email_items is not None:
#             return User.objects.filter(email=email_items)
#         else:
#             # return some queryset
#             pass

class AddImage(views.APIView):

    def post(self,request):
        serializer=user_serializer.ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data=serializer.validated_data
        serializer.instance=services.create_image(image=data)
        print(data)

        return response.Response({"message":"Image Uploaded Succesfully"})


class GetAllImages(views.APIView):
    queryset=ImagesForSlide.objects.all()
    serializer_class=user_serializer.ImageSerializer

    def get(self, request, *args, **kwargs):
      
        UserApi.queryset=ImagesForSlide.objects.all()
                                                 
        

        return self.list(request, *args, **kwargs)


@api_view(["GET","POST"])
def imagesList(request):
    queryset=ImagesForSlide.objects.all()
    serializer=user_serializer.ImageSerializer(queryset,many=True,context={'request': request})

    return response.Response(serializer.data)

    
class RegisterApi(views.APIView):
    
    def post(self,request):


        serializer=user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data=serializer.validated_data
        serializer.instance = services.create_user(user=data)
        print(data)


        # return response.Response(data=serializer.data)
        return response.Response({"message":"Account created Succesfully","user":serializer.data})


    def getData(request,self):
        info = self.post(self,request)
        return info



class LoginAPi(views.APIView):

    def post(self,request):

        email=request.data["email"]
        password=request.data["password"]
       
        user=services.user_email_selector(email=email)
        # cust=RegisterApi.post(self,request);

        if user is None:

            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(raw_password=password):

            raise exceptions.AuthenticationFailed("Invalid Credentials")
        

        # info = RegisterApi.getData()
        token=services.create_token(user_id=user.id)
        resp=response.Response({"token":token,"user": "info"})
        resp.set_cookie(key="jwt",value=token,httponly=True)
        return resp


class UserApi(generics.ListAPIView):

    queryset=User.objects.all()
    serializer_class=user_serializer.UserSerializer

    def get(self, request, *args, **kwargs):
        print( kwargs['search'])
        UserApi.queryset=User.objects.filter(Q(email=kwargs['search']))
                                                 
        

        return self.list(request, *args, **kwargs)



class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)

    permission_classes = (permissions.IsAuthenticated,)


    def post(self,request):
        resp=response.Response()
        resp.delete_cookie("jwt")
        resp.data={"message":"so long farewell"}
        return resp

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    print(user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET","POST"])
def user_api(request,search):
    queryset=User.objects.all()
    serializer=user_serializer.CurrentUserSerializer(queryset,many=False)

    return response.Response(serializer.data)
    # data = {'sample_data': 123}
    # return Response(data, status=HTTP_200_OK)


class Muser(ModelViewSet):
    queryset=User.objects.all()
    serializer_class=user_serializer.CurrentUserSerializer
    lookup_field="email"

    def get_serializer_context(self):
        return {"request":self.request}

class SearchResultWorker(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=user_serializer.UserSerializer

    def get(self, request, *args, **kwargs):
        print( kwargs['search'])
        SearchResultWorker.queryset=User.objects.filter(Q(location__icontains=kwargs['search']))[:1].get()
                                                 
        
        return self.list(request, *args, **kwargs)




# //mpesa api

@api_view(['GET','POST'])

def getAccessToken(request):
    consumer_key='BIi3nqVdy7yzEBEpk7NoAtFi5jXLGIND'
    consumer_secret='d1nTGGqaYYmF5ypG'
    api_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r=requests.get(api_url,auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token=json.loads(r.text)
    validated_mpesa_access_token=mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254745787487,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254745787487,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Mama Fua",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response)

@csrf_exempt
@api_view(['GET','POST'])
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://6079-197-232-61-197.ap.ngrok.io/api/c2b/confirmation",
               "ValidationURL": "https://6079-197-232-61-197.ap.ngrok.io/api/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
@api_view(['GET','POST'])
def call_back(request):
    pass


@csrf_exempt
@api_view(['GET','POST'])
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
@api_view(['GET','POST'])
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
    