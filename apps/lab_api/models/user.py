'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-19 16:12:20
LastEditors: zpliu
LastEditTime: 2022-06-13 14:25:55
@param: 
'''
from django.db import models

# Create your models here.

class Users(models.Model):
    user_name=models.CharField(max_length=30,)
    user_password=models.CharField(max_length=100,)