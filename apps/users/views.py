'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-03-24 21:37:33
LastEditors: zpliu
LastEditTime: 2022-06-17 22:26:14
@param: 
'''
import email
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import json
from .decorators import check_login, check_superuser
from datetime import datetime, timedelta


def user_login(request):
    ''' 
    #? authenticate successful return code 0 and person info
    #? authenticate failed return 1003
    '''
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=email, password=password)
    if user is not None:
        # * login and set session
        login(request, user)
        # * set session
        request.session['IS_LOGIN'] = True
        request.session['IS_SUPERUSER'] = user.check_is_superuser
        # Redirect to a success page.
        response = HttpResponse(json.dumps({
            "code": 0
        }))
        #* setcookie with different roles
        if user.check_is_superuser:
            response.set_cookie(
                'role', 'admin', expires=datetime.now()+timedelta(days=14))
        else:
            response.set_cookie(
                'role', 'editor', expires=datetime.now()+timedelta(days=14))
        return response
    else:
        # Return an 'invalid login' error message.
        return HttpResponse(json.dumps({
            "code": 1003
        }))


def user_add(request):
    '''
    #* several situations occur:
    #? successful register return code 0 and set cookie and session
    #? the passwords do not match return code 1000
    #? something empty return code 1001
    #? user exist change another emial return code 1002
    '''
    User = get_user_model()  # authr user proxy
    password = request.POST.get('password', None)
    repeat_password = request.POST.get('repeat_password', None)
    email = request.POST.get('email', None)
    name = request.POST.get('name', None)
    # * password and repeatPassword don't match
    if password != repeat_password:
        return HttpResponse(
            json.dumps({
                'code': 1000
            })
        )
    if name and email and password and repeat_password:
        # * repeat user check
        if User.objects.filter(email=email):
            return HttpResponse(
                json.dumps({
                    'code': 1002
                })
            )
        else:
            new_user = User.objects.create_user(
                name=name, password=password, email=email)
            new_user.save()
            return HttpResponse(json.dumps({
                'code': 0,
            }))
    else:
        # * something empty
        return HttpResponse(json.dumps({
            'code': 1001
        }))


@check_login
def update_password(request):
    '''permission reject
    '''
    User = get_user_model()
    userid = request.POST['id']
    password=request.POST['password']
    repeatpassword=request.POST['repeatpassword']
    if password!=repeatpassword:
        # * password and repeatPassword don't match
        return HttpResponse(
            json.dumps({
                'code': 1000
            })
        )
    else:
        #* update password
        user=User.objects.get(id=userid)
        user.set_password(password)
        user.save()
        return HttpResponse(json.dumps({'code': 0}))



@check_login
def user_info(request):
    # * get userInfo by sessionID
    User = get_user_model()
    userInfo = User.objects.get(id=request.session.get('_auth_user_id'))
    return HttpResponse(json.dumps({1: 11}))



@check_superuser
def delet_user(request):
    User = get_user_model()
    userId = request.POST.get("id", None)
    deleteResult = User.objects.filter(id=userId).delete()
    if deleteResult:
        # * successful
        return HttpResponse(json.dumps({1: 11}))
    else:
        # * failed
        return HttpResponse(json.dumps({1: 0}))


def logout_user(request):
    logout(request)
    return HttpResponse(json.dumps({1: 0}))



def update_userInfo(request):
    return  HttpResponse(json.dumps({1: 0}))
