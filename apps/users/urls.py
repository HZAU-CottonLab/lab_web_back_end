'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 20:22:42
LastEditors: zpliu
LastEditTime: 2022-07-06 15:51:23
@param: 
'''
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('roles/', views.get_user_roles),
    path('register/', views.user_add),
    path('password/', views.update_password),
    path('info/', views.user_info),
    path('delete/',views.delet_user),
    path('logout/',views.logout_user),
    path('update/',views.update_userInfo),
    # path('icon/upload/',views.image_upload),
    # path('icon/delete/',views.image_delete),
    path('teachers/',views.show_teachers),
    path('team/',views.show_team),
]