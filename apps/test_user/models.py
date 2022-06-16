'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 21:45:03
LastEditors: zpliu
LastEditTime: 2022-06-16 21:55:28
@param: 
'''
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from pymysql import NULL
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    sex_choise = (
        (0, "男"),
        (1, "女"),
    )
    peopleType = (
        (0, '老师'),
        (1, '博士后'),
        (2, '博士'),
        (3, '硕士'),
        (4, '访问学者'),
    )
    name = models.CharField(max_length=30, blank=False,default="None")
    sex = models.IntegerField( choices=sex_choise, blank=True, null=NULL)
    img_url = models.CharField(blank=True, max_length=30, null=NULL)
    people_type = models.IntegerField(
        choices=peopleType, blank=True, null=NULL)
    contact = models.CharField(max_length=50, blank=True, null=NULL)
    office_site = models.CharField(max_length=100, blank=True, null=NULL)
    info_detail = models.CharField(max_length=100, blank=True, null=NULL)
    #* email 用作用户身份的唯一标识符
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email