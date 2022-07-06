'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-03-24 21:37:33
LastEditors: zpliu
LastEditTime: 2022-07-06 16:35:39
@param: 
'''
import os
from django.conf import settings
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
import json
from .decorators import check_login, check_superuser
from datetime import datetime, timedelta
from picture.models import customer_picture
from users.models import User, UserPicture


def user_login(request):
    ''' 
    #? authenticate successful return code 0 and person info
    #? authenticate failed return 1003
    '''
    # print(request.__dict__)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # * login and set session
            login(request, user)
            # * set session
            request.session['IS_LOGIN'] = True
            request.session['IS_SUPERUSER'] = user.check_is_superuser
            request.session['USER_ID'] = user.id
            # Redirect to a success page.
            response = HttpResponse(json.dumps({
                "errno": 0,
                "accessToken": 111111111111,
                "info": {
                    "username": user.name,
                    "id": user.id,
                    "loginStatus": True,
                }

            }))
            # * setcookie with different roles
            # if user.check_is_superuser:
            #     response.set_cookie(
            #         'role', 'admin', expires=datetime.now()+timedelta(days=14))
            # else:
            #     response.set_cookie(
            #         'role', 'editor', expires=datetime.now()+timedelta(days=14))
            return response
        else:
            # Return an 'invalid login' error message.
            return HttpResponse(json.dumps({
                "errno": 1003,
                "message": "账号或密码错误"
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
    repeat_password = request.POST.get('repeatPassword', None)
    email = request.POST.get('email', None)
    name = request.POST.get('name', None)
    # * password and repeatPassword don't match
    if password != repeat_password:
        return HttpResponse(
            json.dumps({
                'errno': 1000,
                'message': "两次密码输入不一致"
            })
        )
    if name and email and password and repeat_password:
        # * repeat user check
        if User.objects.filter(email=email):
            return HttpResponse(
                json.dumps({
                    'errno': 1002,
                    'message': "账号已经注册"
                })
            )
        else:
            new_user = User.objects.create_user(
                name=name, password=password, email=email)
            new_user.save()
            return HttpResponse(json.dumps({
                'errno': 0,
                'message': "注册成功"
            }))
    else:
        # * something empty
        return HttpResponse(json.dumps({
            'errno': 1001,
            'message': "缺少必填项"
        }))


@check_login
def update_password(request):
    '''permission reject
    '''
    User = get_user_model()
    userid = request.POST['id']
    password = request.POST['password']
    repeatpassword = request.POST['repeatpassword']
    if password != repeatpassword:
        # * password and repeatPassword don't match
        return HttpResponse(
            json.dumps({
                'errno': 1000,
                'message': "两次密码输入不一致"
            })
        )
    else:
        # * update password
        user = User.objects.get(id=userid)
        user.set_password(password)
        user.save()
        return HttpResponse(json.dumps({'code': 0}))


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


@check_login
def update_userInfo(request):
    '''update User info
    '''
    User = get_user_model()
    userId = request.POST.get("id", None)
    userInfo = User.objects.filter(id=userId)
    teacherId = request.POST.get("teacher", -1)
    # -----------------------------
    # 检测更新的用户信息与登录账户是否相同
    # -----------------------------
    if request.session['USER_ID'] != int(userId):
        return HttpResponse(
            json.dumps(
                {'errno': 1010,
                 "message": "无操作权限"
                 }
            )
        )
    if teacherId == '':
        # 导师编号为空的情况
        teacherId = -1
    imgURL = request.POST.get("imgURL", None).replace(settings.WEB_URL, '')
    PictureObject = customer_picture.objects.filter(
        img_url__exact=imgURL
    ).first()
    if userInfo and PictureObject:
        # * update partion fields,
        existedImg = userInfo[0].avatar
        existedImg = existedImg.replace(settings.WEB_URL, '')
        userInfo.update(
            name=request.POST.get("name", None),
            sex=request.POST.get("sex", 0),
            people_type=request.POST.get("peopleType", None),
            contact=request.POST.get("contact", None),
            office_site=request.POST.get("officeSite", None),
            info_detail=request.POST.get("infoDetail", None),
            recruit=request.POST.get("recruit", None),
            teacher=teacherId,
            jobTitle=request.POST.get("jobTitle", None),
        )
        if existedImg != imgURL:
            # * 修改relationship，并删除原有的PictureObject
            userInfo[0].img_url.all().filter(alt="avatar").delete()
            userInfo[0].img_url.add(PictureObject)
        return HttpResponse(
            json.dumps(
                {'errno': 0,
                 "message": "数据已经保存"
                 }
            )
        )
    elif not PictureObject:
        return HttpResponse(
            json.dumps({
                'errno': 1006,
                "message": "图片未上传，或已删除!"
            }))
    else:
        return HttpResponse(json.dumps(
            {'errno': 1004,
             "message": "用户不存在"
             }))


# @check_login
# def image_upload(request):
#     if request.method == 'POST':
#         print(request.content_type)
#         # print(request.body)
#         Picture = request.FILES.get("image")
#         User = get_user_model()
#         # * upload the image file and save the picture in disk and update the model
#         PictureObject = customer_picture.objects.uploadImg(Picture)
#         userId = request.POST.get("id", None)
#         # *
#         userObject = User.objects.get(id=userId)
#         if not userObject:
#             return HttpResponse(json.dumps({'errno': 1004}))
#         else:
#             # * save the relationship
#             userObject.img_url.add(PictureObject)
#             # * save the relationshipr bettwwn picture and user
#             # TODO filter the image URL
#             return HttpResponse(json.dumps({
#                 "errno": 0,
#                 "data": {
#                     "url": userObject.avatar
#                 }
#             }))


# @check_login
# def image_delete(request):
#     if request.method == 'POST':
#         User = get_user_model()
#         userId = request.POST.get("id", None)
#         userObject = User.objects.get(id=userId)
#         if not userObject:
#             return HttpResponse(json.dumps({'errno': 1004}))
#         else:
#             # * delete the relationship and remove from disk
#             for i in userObject.img_url.all():
#                 i.delete()
#             return HttpResponse(json.dumps({
#                 "errno": 0,

#             }))


def user_is_checked(request):
    '''
    '''
    pass
    return HttpResponse(json.dumps({1: 0}))


@check_login
def logout_user(request):
    logout(request)
    return HttpResponse(
        json.dumps({
            "errno": 0,
            "message": ""
        }))


@check_login
def get_user_roles(request):
    User = get_user_model()
    userId = request.session['_auth_user_id']
    # * use session to login
    userObject = User.objects.get(id=userId)
    if userObject.check_is_superuser:
        return HttpResponse(json.dumps({
            "errno": 0,
            "roles": ['admin'],
            'id': userObject.id,
            'name': userObject.name,
            'message': ''
        }))
    else:
        return HttpResponse(json.dumps({
            "errno": 0,
            "roles": ['editor'],
            'id': userObject.id,
            'name': userObject.name,
            'message': ''
        }))

# -----------------------------------------------------
# don't required authenticate
# -----------------------------------------------------


def user_info(request):
    # * get user information by userID
    User = get_user_model()
    userid = request.POST['id']
    userInfo = User.objects.get(id=userid)
    if not userInfo:
        # * no such User
        return HttpResponse(json.dumps({'errno': 1004}))
    else:
        # * the first picture of the person

        return HttpResponse(json.dumps(
            {
                'errno': 0,
                'info': {
                    'basic': {
                        "id": userInfo.id,
                        "name": userInfo.name,
                        "imgURL": userInfo.avatar,
                        "sex": str(userInfo.sex),
                        "peopleType": str(userInfo.people_type),
                        "jobTitle": userInfo.jobTitle,
                        "contact": userInfo.contact,
                        "officeSite": userInfo.office_site,
                        "teacher": userInfo.teacher,
                        "teacher_nickname":userInfo.teacher_nickname
                    },
                    'infoDetail': json.loads(userInfo.info_detail),
                }
            }
        ))


def show_teachers(request):
    # * 查找所有为teacher的项
    User = get_user_model()
    teacherObjects = User.objects.filter(people_type=0)
    teacherList = []
    for teacher in teacherObjects:
        teacherList.append({
            'id': teacher.id,
            'name': teacher.name,
            'imageURL': teacher.avatar

        })
    return HttpResponse(json.dumps({
        'errno': 0,
        "data": teacherList
    }))


def show_team(request):
    # * 获取所有人员信息
    UserObject = get_user_model()
    userArray = []

    for peopleTypeDict in UserObject.objects.exclude(
        people_type__isnull=True
    ).values('people_type').distinct():
        peopleTypeId = peopleTypeDict.get('people_type')
        user_set = UserObject.objects.filter(people_type=peopleTypeId)
        PeopleDict = {
            'id': peopleTypeId,
            'title': user_set.first().get_people_type_display(),
            'peopleInfos': []
        }
        for userInstance in user_set:
            PeopleDict['peopleInfos'].append(
                userInstance.info
            )
        userArray.append(
            PeopleDict
        )
    return HttpResponse(json.dumps({
        'errno': 0,
        'info': userArray
    }))
