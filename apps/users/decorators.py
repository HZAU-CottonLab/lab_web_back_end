'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-17 20:44:14
LastEditors: zpliu
LastEditTime: 2022-06-17 22:02:27
@param: 
'''

from django.shortcuts import HttpResponse
import json


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if request.session.get("IS_LOGIN", False):
            return fn(request, *args, **kwargs)
        else:
            #* login required
            return HttpResponse(json.dumps({
                "code": 999
            }))
    return wrap

def check_superuser(fn):
    def wrap(request,*args,**kwargs):
        if request.session.get('IS_SUPERUSER',False):
            return fn(request,*args,**kwargs)
        else:
            #* no permission
            return HttpResponse(json.dumps({
                "code": 1005
            }))
    return wrap