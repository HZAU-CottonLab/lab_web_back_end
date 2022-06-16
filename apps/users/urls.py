'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 20:22:42
LastEditors: zpliu
LastEditTime: 2022-06-16 22:35:52
@param: 
'''
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('register/', views.user_add),
    path('password/', views.update_password),
    path('info/', views.user_info),
]