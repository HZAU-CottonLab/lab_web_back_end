'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-24 09:47:55
LastEditors: zpliu
LastEditTime: 2022-06-24 14:46:34
@param: 
'''


from django.shortcuts import HttpResponse
# Create your views here.
import json
from picture.models import customer_picture


def uploadPicture(request):
    if request.method == 'POST':
        # print(request.body)
        Picture = request.FILES.get("image")
        # * alt of the picture
        alt = request.POST.get('alt', 'picture.alt')
        # * upload the image file and save the picture in disk and update the model
        PictureObject = customer_picture.objects.uploadImg(Picture, alt)
        return HttpResponse(json.dumps({
            "errno": 0,
            "data": {
                "url": PictureObject.url
            }
        }))
