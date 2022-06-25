'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-24 09:47:59
LastEditors: zpliu
LastEditTime: 2022-06-24 09:53:39
@param: 
'''
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.uploadPicture),
    # path('teachers/',views.show_team),
]