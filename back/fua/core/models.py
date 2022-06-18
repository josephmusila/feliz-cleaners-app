from django.db import models
from django.contrib.auth import models as auth_models

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
    username=None


    objects = UserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["first_name","last_name"]