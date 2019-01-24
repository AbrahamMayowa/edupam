from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserInfo
from .forms import UserForm, ChangeUser


class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    form = ChangeUser
    model = UserInfo


admin.site.register(UserInfo, CustomUserAdmin)




# Register your models here.
