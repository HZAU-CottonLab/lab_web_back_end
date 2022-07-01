'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-24 09:25:02
LastEditors: zpliu
LastEditTime: 2022-06-28 19:52:29
@param: 
'''
from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.news_add),
    path('all/',views.get_all_news),
    path('info/',views.get_news_byId),
    path('update/',views.news_update),
    path('delete/',views.del_news_by_Id),
    path("check/",views.news_checked),
    path("carousel/",views.carousel_list),
    path("latest/",views.latest_news),
]
