import dataclasses
from . import models
from django.conf import settings
import jwt
from datetime import datetime
from datetime import timedelta
# import datetime

datetime.utcnow()
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass

class UserDataClass:
    first_name: str
    last_name: str
    email: str
    phone: str
    email: str
    password: str = None
    id: int=None

    @classmethod
    def from_instance(cls,user:"User")->"UserDataClass":
        return cls(first_name=user.first_name,last_name=user.last_name,email=user.email,phone=user.phone,id=user.id)

def create_user(user:"UserDataClass") ->"UserDataClass":
    instance=models.User(first_name=user.first_name,last_name=user.last_name,email=user.email)

    if user.password is not None:
        instance.set_password(user.password)

    instance.save()
    return UserDataClass.from_instance(instance)


def user_email_selector(email:str)->"User":
    user=models.User.objects.filter(email=email).first()

    return user
def create_token(user_id:int)->str:
    payload = dict(id=user_id, exp=datetime.utcnow() + timedelta(hours=24),iat=datetime.utcnow())

    
    token=jwt.encode(payload,settings.JWT_SECRET, algorithm="HS256")
    return token
