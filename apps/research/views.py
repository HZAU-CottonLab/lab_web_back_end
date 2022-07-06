'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-25 21:41:49
LastEditors: zpliu
LastEditTime: 2022-07-06 17:38:02
@param: 
'''
from django.shortcuts import HttpResponse
import json
from django.conf import settings
from picture.models import customer_picture
from research.models import Research
from users.decorators import check_superuser,check_login
# Create your views here.
booleanDict = {
    'true': 1,
    'false': 0
}

@check_login
@check_superuser
def research_add(request):
    title = request.POST.get("title", None)
    description = request.POST.get("description", None)
    date = request.POST.get("date", None)
    # * 初始化时默认处于审核状态
    # * 完整的访问路径
    imgURL = request.POST.get("imageURL", None).replace(settings.WEB_URL, '')
    PictureObject = customer_picture.objects.filter(
        img_url__exact=imgURL
    ).first()
    if PictureObject:
        ResearchInstance = Research.objects.create(
            title=title,
            description=description,
            date=date,
            PictureObject=PictureObject
        )
        return HttpResponse(json.dumps({
            'errno': 0,
            "message": "数据已保存",
            "data": ResearchInstance.id
        }))
    else:
        return HttpResponse(
            json.dumps({
                'errno': 1006,
                "message": "图片未上传，或已经删除!"
            })
        )

@check_login
@check_superuser
def research_update(request):
    researchId = request.POST.get('id', None)
    researchInstatnce = Research.objects.filter(id=researchId)
    imgURL = request.POST.get("imageURL", None).replace(settings.WEB_URL, '')
    # * 当前上传的图片对应的models实例
    PictureObject = customer_picture.objects.filter(
        img_url__exact=imgURL).first()
    if researchInstatnce and PictureObject:
        existedImg = researchInstatnce[0].data['imageURL']
        existedImg = existedImg.replace(settings.WEB_URL, '')
        # * 图片不改外，其他字段批量改动
        researchInstatnce.update(
            title=request.POST.get("title", None),
            description=request.POST.get("description", None),
            date=request.POST.get("date", None),
        )
        if existedImg != imgURL:
            researchInstatnce[0].imageURL.all().filter(alt="avatar").delete()
            researchInstatnce[0].imageURL.add(PictureObject)
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "research已更新!"
            }))
    elif not PictureObject:
        return HttpResponse(
            json.dumps({
                'errno': 1006,
                "message": "图片未上传，或已经删除!"
            })
        )
    else:
        return HttpResponse(
            json.dumps({
                'errno': 1009,
                "message": "rearch 已经删除或者不存在!"
            }))


def queryResearchById(request):
    researchId = request.POST.get('id', None)
    requestObject = Research.objects.filter(id=researchId).first()
    if requestObject:
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "research信息!",
                "data": requestObject.data
            }))
    else:
        return HttpResponse(
            json.dumps({
                'errno': 1009,
                "message": "rearch 已经删除或者不存在!"
            }))


def get_all_researchItems(request):
    researchItems = Research.objects.all()
    content = []
    for item in researchItems:
        content.append(item.data)
    return HttpResponse(
        json.dumps({
            'errno': 0,
            "message": "rearch列表",
            'content': content
        }))

@check_login
@check_superuser
def researchItem_delete(request):
    researchId = request.POST.get("id", None)
    try:
        researchInstance = Research.objects.get(id=researchId)
        for i in researchInstance.imageURL.all():
            # 删除与其关联的所有图片
            i.delete()
        researchInstance.delete()
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "Research已删除!"
            }))
    except Research.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1009,
                "message": "Research不存在!"
            }))

@check_login
@check_superuser
def research_check(request):
    researchId = request.POST.get("id", None)
    check = request.POST.get("check", None)
    try:
        researchInstance = Research.objects.get(id=researchId)
        researchInstance.is_check = booleanDict.get(check, 0)
        researchInstance.save()
        return HttpResponse(json.dumps({
            'errno': 0,
            "message": "审核状态已改变"
        }))
    except Research.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1009,
                "message": "Research不存在!"
            }))
