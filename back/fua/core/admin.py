from django.contrib import admin
from . import models

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display=("id","first_name","last_name","email",)

admin.site.register(models.User,UserAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display=("id","label","image",)

admin.site.register(models.ImagesForSlide,ImageAdmin)
admin.site.register(models.MpesaPayment)
