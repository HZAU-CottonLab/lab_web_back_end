'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-25 16:55:01
LastEditors: zpliu
LastEditTime: 2022-07-06 17:49:20
@param: 
'''
from django.shortcuts import HttpResponse
import json
from publication.models import publication
# Create your views here.
from users.decorators import check_login,check_superuser
@check_login
@check_superuser
def add(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    periodical = request.POST.get('periodical')
    date = request.POST.get('date')
    doi = request.POST.get('doi')
    publication.objects.create(
        title, author, periodical, date, doi
    )
    return HttpResponse(
        json.dumps({
            'errno': 0,
            "message": "文献已保存"
        })
    )



@check_login
@check_superuser
def publication_update(request):
    try:
        publicationInstance = publication.objects.filter(
            id=request.POST.get('id', None))
        title = request.POST.get('title')
        author = request.POST.get('author')
        periodical = request.POST.get('periodical')
        date = request.POST.get('date')
        doi = request.POST.get('doi')
        publicationInstance.update(
            title=title,
            author=author,
            periodical=periodical,
            date=date,
            doi=doi
        )
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "数据已经更新",
            }))
    except publication.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1008,
                "message": "文献已删除，或不存在"
            })
        )



@check_login
@check_superuser
def delete_publication_byID(request):
    try:
        publication.objects.get(id=request.POST.get('id', None)).delete()
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "数据已删除",
            })
        )
    except publication.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1008,
                "message": "文献已删除，或不存在"
            })
        )

def publication_byId(request):
    try:
        publicationInstance = publication.objects.get(
            id=request.POST.get('id', None))
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "",
                "data": publicationInstance.data

            }))
    except publication.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1008,
                "message": "文献已删除，或不存在"
            })
        )
def get_all_publication(request):
    publicationData = {}
    publicationObjects = publication.objects.all()
    # * 按照年份合并数据
    for publicationInstance in publicationObjects:
        publicationData[publicationInstance.year] = publicationData.get(
            publicationInstance.year, [])
        publicationData[publicationInstance.year].append(
            publicationInstance.data
        )
    responseData = []
    for key, value in publicationData.items():
        responseData.append(
            {
                "year": key,
                "content": value
            }
        )
    return HttpResponse(
        json.dumps({
            'errno': 0,
            "message": "获取所有文献信息",
            "data": responseData
        })
    )