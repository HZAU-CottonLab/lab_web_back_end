'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-03-24 21:37:33
LastEditors: zpliu
LastEditTime: 2022-06-16 22:55:50
@param: 
'''
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import json


def user_login(request):
    ''' 
    #? authenticate successful return code 0 and person info
    #? authenticate failed return 1003
    '''
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        #* login and set session
        login(request, user)
        # Redirect to a success page.
        return HttpResponse(json.dumps({
            "code":0
        }))
    else:
        # Return an 'invalid login' error message.
          return HttpResponse(json.dumps({
            "code":1003
        }))


def user_add(request):
    '''
    #* several situations occur:
    #? successful register return code 0 and set cookie and session
    #? the passwords do not match return code 1000
    #? something empty return code 1001
    #? user exist change another emial return code 1002
    '''
    User=get_user_model()   #authr user proxy
    password = request.POST.get('password', None)
    repeat_password = request.POST.get('repeat_password', None)
    email = request.POST.get('email', None)
    name = request.POST.get('name', None)
    #* don't match 
    if password!=repeat_password:
        return HttpResponse(
            json.dumps({
                'code':1000
            })
        )
    if name and email and password and repeat_password:
        #* repeat user check
        if  User.objects.filter(email=email):
            return HttpResponse(
                json.dumps({
                    'code':1002
                })
            )
        else:
            new_user = User.objects.create_user(
            name=name, password=password, email=email)
            new_user.save() 
            return HttpResponse(json.dumps({
                'code':0,
            }))
    else:
        #* something empty
        return HttpResponse(json.dumps({
            'code':1001
        }))


def update_password(request):
    '''permission reject
    '''
    User=get_user_model()
    print(request.session.get('IS_LOGIN'))
    name = request.POST['email']
    print(request.user)
    # u=User.objects.get(name=name)
    # u.set_password('11')
    # u.save()
    return HttpResponse(json.dumps({1: 11}))



def user_info(request):
    #* get userInfo by sessionID
    User=get_user_model()
    if request.session.get('_auth_user_id'):
        #* 获取用户所有字段的数据
        userInfo=User.objects.get(id=request.session.get('_auth_user_id'))
        print(userInfo.__dict__)
        pass 
    else:
        pass 
    return HttpResponse(json.dumps({1: 11}))