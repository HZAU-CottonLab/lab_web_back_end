'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-05-28 22:13:15
LastEditors: zpliu
LastEditTime: 2022-05-28 22:23:06
@param: 
'''
from django.shortcuts import HttpResponse
import json
def test_post(request):
    if request.method == 'POST':
            return HttpResponse(json.dumps({
                "code":200,
            }))
    else:            
            return HttpResponse(json.dumps({
                "code":500,
            }))
def test_get(request):
    if request.method == 'get':
            return HttpResponse(json.dumps({
                "code":200,
            }))
    else:
            return HttpResponse(json.dumps({
                "code":500,
            }))
