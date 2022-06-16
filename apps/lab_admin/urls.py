'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-19 16:33:12
LastEditors: zpliu
LastEditTime: 2021-10-19 16:37:30
@param: 
'''
from django.urls import path 
from . import views
urlpatterns = [
    path('add_user', views.add_user,name='add_user'),
]