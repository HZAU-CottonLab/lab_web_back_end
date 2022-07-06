'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-17 20:44:14
LastEditors: zpliu
LastEditTime: 2022-07-06 17:47:27
@param: 
'''


from fileinput import filename
from django.shortcuts import HttpResponse
import json
import os
import hashlib

import django.utils.timezone as timezone
from django.conf import settings



def check_login(fn):
    def wrap(request, *args, **kwargs):
        if request.session.get("IS_LOGIN", False):
            return fn(request, *args, **kwargs)
        else:
            # * login required
            return HttpResponse(json.dumps({
                "errno": 999,
                "message":"请先登录，再执行操作"
            }))
    return wrap


def check_superuser(fn):
    def wrap(request, *args, **kwargs):
        if request.session.get('IS_SUPERUSER', False):
            return fn(request, *args, **kwargs)
        else:
            # * no permission
            return HttpResponse(json.dumps({
                "code": 1005,
                "message":"抱歉，您无权限访问"
            }))
    return wrap


