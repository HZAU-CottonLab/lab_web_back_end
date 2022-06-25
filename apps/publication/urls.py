'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-25 16:54:38
LastEditors: zpliu
LastEditTime: 2022-06-25 20:46:02
@param: 
'''
from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add),
    path('info/',views.publication_byId),
    path('update/',views.publication_update),
    path('all/',views.get_all_publication),
    path('delete/',views.delete_publication_byID),
]
