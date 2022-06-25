'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-17 20:35:47
LastEditors: zpliu
LastEditTime: 2022-06-25 21:42:36
@param: 
'''
from operator import imod
from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from . import settings
from django.urls import path
import apps.users.urls as user
# import apps.lab_admin.urls as lab_admin_urls
import apps.news.urls as news
import apps.picture.urls as picture
import apps.publication.urls as publication
import apps.research.urls as research
urlpatterns = [
    path('user/', include(user),name='userAPI'),
    path('news/', include(news),name='newsAPI'),
    path('img/', include(picture),name='picture'),
    path('publication/', include(publication),name='publication'),
    path('research/', include(research),name='research'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)