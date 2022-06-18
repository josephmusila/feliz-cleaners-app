from django.urls import path
from . import apis


urlpatterns = [
    path("register/",apis.RegisterApi.as_view(),name="register"),
    path("login/",apis.LoginAPi.as_view(),name="login"),
    path("user/",apis.UserApi.as_view(),name="user"),
    path("logout/",apis.LogoutApi.as_view(),name="logout"),
    path("users/account=<str:email>/",apis.GetUser.as_view(),name="custuser")
]
