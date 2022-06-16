'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-17 20:35:47
LastEditors: zpliu
LastEditTime: 2022-06-16 20:24:41
@param: 
'''
"""lab_web_back_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
import apps.users.urls as user
import apps.lab_admin.urls as lab_admin_urls

urlpatterns = [
    path('user/', include(user),name='userAPI'),
]
