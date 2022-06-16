'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-17 20:38:45
LastEditors: zpliu
LastEditTime: 2022-06-14 22:33:58
@param: 
'''
from django.urls import path
from lab_api.Users import view as User_view

urlpatterns = [
    path('user/login/', User_view.user_login),
    path('register/', User_view.user_add),
    path('user/password/', User_view.update_password),
]
