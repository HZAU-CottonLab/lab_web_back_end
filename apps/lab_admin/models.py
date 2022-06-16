'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-19 16:12:20
LastEditors: zpliu
LastEditTime: 2021-10-19 17:11:06
@param: 
'''
from django.db import models

# Create your models here.

class Users(models.Model):
    user_name=models.CharField(max_length=30,)
    user_password=models.CharField(max_length=100,)
    def __str__(self) -> str:
        return self.user_name