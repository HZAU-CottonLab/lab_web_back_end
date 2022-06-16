'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-14 19:24:23
LastEditors: zpliu
LastEditTime: 2022-06-14 19:24:24
@param: 
'''
from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
