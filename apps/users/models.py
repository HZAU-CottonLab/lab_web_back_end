'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 16:34:41
LastEditors: zpliu
LastEditTime: 2022-06-16 22:09:26
@param: 
'''


from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from pymysql import NULL
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractBaseUser,PermissionsMixin):
    '''
    #* email primary key
    #* username
    '''
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
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=30, blank=False,default="None")
    sex = models.IntegerField( choices=sex_choise, blank=True, null=NULL)
    img_url = models.CharField(blank=True, max_length=30, null=NULL)
    people_type = models.IntegerField(
        choices=peopleType, blank=True, null=NULL)
    contact = models.CharField(max_length=50, blank=True, null=NULL)
    office_site = models.CharField(max_length=100, blank=True, null=NULL)
    info_detail = models.CharField(max_length=100, blank=True, null=NULL)
    is_active = models.BooleanField(default=True)
    #* unique validate field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
