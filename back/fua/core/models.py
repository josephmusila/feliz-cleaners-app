from django.db import models
from django.contrib.auth import models as auth_models
# from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings


class UserManager(auth_models.BaseUserManager):
    def create_user(self, first_name:str, last_name:str, email:str, password:str = None,is_staff=False,is_superUser=False)->"User":
        if not email:
            raise ValueError ("User Must Have an Email")
        if not first_name:
            raise ValueError ("User Must Have a First Name")
        if not last_name:
            raise ValueError ("User Must Have a Last Name")

        user=self.model(email=self.normalize_email(email))
        user.first_name=first_name
        user.last_name=last_name
        user.set_password(password)
        user.is_active=True
        user.is_staff=is_staff
        user.is_superuser=is_superUser
        user.save()


        return user

    def create_superuser(self, first_name:str, last_name:str, email:str, password:str)->"User":
        user=self.create_user(first_name=first_name, last_name=last_name, email=email,password=password, is_superUser=True, is_staff=True,)

        user.save()
        return user
       

class User(auth_models.AbstractUser):
    first_name=models.CharField(verbose_name="First Name",max_length=200)
    last_name=models.CharField(verbose_name="Last Name",max_length=250)
    email=models.EmailField(verbose_name="Email",max_length=255,unique=True)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=50)
    avatar=models.ImageField(upload_to="uploads",blank=True,null=True)
    location=models.CharField(max_length=255,blank=False,null=False)
    username=None
    


    objects = UserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["first_name","last_name"]


    # @property

    # def token(self):
    #     token= jwt.encode({"email":self.email,"location":self.location,"exp":datetime.utcnow() + timedelta(hours=24)},settings.SECRET_KEY,algorithms=['HS256'] )

    #     return token


class ImagesForSlide(models.Model):
    label=models.CharField(max_length=300,blank=True,null=True)
    image=models.ImageField(upload_to="uploads",blank=True,null=True)



# payments models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'

class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'



class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name