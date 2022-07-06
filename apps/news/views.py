
from django.shortcuts import HttpResponse
# Create your views here.
import json
from django.conf import settings
from picture.models import customer_picture
from news.models import News
from django.db.models import Q
from users.decorators import check_login,check_superuser


booleanDict = {
    'true': 1,
    'false': 0
}

@check_login
@check_superuser
def news_add(request):
    title = request.POST.get("title", None)
    description = request.POST.get("description", None)
    vhtml = request.POST.get("vhtml", None)
    date = request.POST.get("date", None)
    latest = request.POST.get("latest", None)
    check = request.POST.get("check", None)
    # * 完整的访问路径
    imgURL = request.POST.get("imageURL", None).replace(settings.WEB_URL, '')
    # * get Picture Object
    # * alt=avatar 表示首页图片
    PictureObject = customer_picture.objects.filter(
        img_url__exact=imgURL
    ).first()
    check = booleanDict.get(check, 0)
    latest = booleanDict.get(latest, 0)
    if PictureObject:
        newsInstance = News.objects.news_add(
            title,
            description,
            vhtml,
            date,
            latest,
            check,
            PictureObject
        )
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "数据已保存",
                "data": newsInstance.id
            })
        )
    else:
        return HttpResponse(
            json.dumps({
                'errno': 1006,
                "message": "图片未上传，或已经删除!"
            })
        )

@check_login
@check_superuser
def news_update(request):
    # * 检测当前的avatar是否与已有的avatar一致；
    # * 如果不一致则删除原有的并更新image
    newsId = request.POST.get("id", None)
    newsInstance = News.objects.filter(id=newsId)
    # * 查找该图片对应的Picture Object
    imgURL = request.POST.get("imageURL", None).replace(settings.WEB_URL, '')

    PictureObject = customer_picture.objects.filter(
        img_url__exact=imgURL
    ).first()
    if newsInstance and PictureObject:
        existedImg = newsInstance[0].data['imageURL']
        existedImg = existedImg.replace(settings.WEB_URL, '')
        # 头像未改动,其他字段批量修改
        newsInstance.update(
            title=request.POST.get("title", None),
            description=request.POST.get("description", None),
            vhtml=request.POST.get("vhtml", None),
            date=request.POST.get("date", None),
            latest=booleanDict.get(request.POST.get("latest", 'false')),
            is_check=booleanDict.get(request.POST.get("check", 'false'))
        )
        if existedImg != imgURL:
            # * 修改relationship，并删除原有的PictureObject
            newsInstance[0].imageURL.all().filter(alt="avatar").delete()
            newsInstance[0].imageURL.add(PictureObject)
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "新闻已更新!"
            }))

    elif not PictureObject:
        return HttpResponse(
            json.dumps({
                'errno': 1006,
                "message": "图片未上传，或已删除!"
            }))
    else:
        return HttpResponse(
            json.dumps({
                'errno': 1007,
                "message": "新闻已删除!"
            }))


def get_all_news(request):
    newObjects = News.objects.all()
    newsData = []
    for item in newObjects:
        # 每张表可能有多个picture，筛选alt为avatar的图片
        newsData.append(
            item.data
        )
    return HttpResponse(
        json.dumps({
            'errno': 0,
            "message": "请求新闻列表",
            "data": newsData
        })
    )


def get_news_byId(request):
    newsObject = News.objects.filter(Q(id=request.POST.get("id", None))&Q(is_check=True)).first()
    if newsObject:
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "请求新闻信息",
                "data": newsObject.data
            })
        )
    else:
        return HttpResponse(
            json.dumps({
                'errno': 1007,
                "message": "请求的新闻不存在!"
            }))

@check_login
@check_superuser
def del_news_by_Id(request):
    newsId = request.POST.get("id", None)
    try:
        newsInstance = News.objects.get(id=newsId)
        for i in newsInstance.imageURL.all():
            # 删除与其关联的所有图片
            i.delete()
        newsInstance.delete()
        return HttpResponse(
            json.dumps({
                'errno': 0,
                "message": "新闻已删除!"
            }))
    except News.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1007,
                "message": "新闻不存在!"
            }))
@check_login
@check_superuser
def news_checked(request):
    newsId = request.POST.get("id", None)
    check=request.POST.get("check", None)
    try:
        newsInstance = News.objects.get(id=newsId)
        newsInstance.is_check=booleanDict.get(check,0)
        newsInstance.save()
        return HttpResponse(json.dumps({
                'errno': 0,
                "message": "审核状态已改变"
            }))
    except News.DoesNotExist:
        return HttpResponse(
            json.dumps({
                'errno': 1007,
                "message": "新闻不存在!"
            })) 

def carousel_list(request):
    newsList=News.objects.filter(Q(latest=True) & Q(is_check=True))
    if newsList:
        carouselList=[i.data for i in newsList]
        return HttpResponse(
                json.dumps({
                    'errno': 0,
                    "message": "查询Carousel列表",
                    "data":carouselList

                }))  
    else:
        return HttpResponse(
                json.dumps({
                    'errno': 1007,
                    "message": "新闻不存在!"
                })) 


def latest_news(request):
    #除去放在跑马灯中的新闻
    newsList=News.objects.filter(
        Q(latest=False) &Q(is_check=True)
    )
    if newsList:
        latestList=[i.data for i in newsList[0:3]]
        return HttpResponse(
                json.dumps({
                    'errno': 0,
                    "message": "查询latest列表",
                    "data":latestList

                }))  
    else:
        return HttpResponse(
                json.dumps({
                    'errno': 1007,
                    "message": "新闻不存在!"
                })) 

