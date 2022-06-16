'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-19 16:30:51
LastEditors: zpliu
LastEditTime: 2021-10-19 17:00:15
@param: 
'''
from django.shortcuts import render
from lab_admin.models import Users
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def getPostDict(request):
    '''
    #! if data with post methods 
    '''
    if request.method == 'POST':
        try:
            # ? Content-Disposition: x-www-form-urlencoded (default)
            request_data = request.body
            request_dict = json.loads(request_data.decode('utf-8'))
        except Exception as result:
            # ?Content-Disposition: form-data
            request_dict = request.POST
        return request_dict
    else:
        return request
# Create your views here.

# @csrf_exempt #局部禁用csrf
def add_user(request):
    requestDict = getPostDict(request=request)
    #? cread the 
    u = Users(
        user_name=requestDict['user_name'],
        user_password=requestDict['password'])
    u.save()        
    print(Users.objects.all())
    return JsonResponse({
        'dsad':0
    })

