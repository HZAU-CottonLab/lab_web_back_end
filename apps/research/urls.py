'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-25 21:39:32
LastEditors: zpliu
LastEditTime: 2022-06-25 22:41:43
@param: 
'''
from django.urls import path
from . import views 
urlpatterns = [
    path("add/",views.research_add),
    path("info/",views.queryResearchById),
    path("update/",views.research_update),
    path("all/",views.get_all_researchItems),
]