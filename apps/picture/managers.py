'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-20 14:30:54
LastEditors: zpliu
LastEditTime: 2022-06-24 14:40:53
@param: 
'''
from django.db import models
import os
from django.conf import settings
import django.utils.timezone as timezone
import hashlib
# from .models import customer_picture as customer_picture
# print(1)
# from .models import user_picture as UserPicture


def upload_picture(file):
    # * dirPath check
    ext = file.name.split('.')[-1]
    year = timezone.now().year
    month = timezone.now().month
    day = timezone.now().day
    subPath = "{}/{}/{}".format(year, month, day)
    FilePath = os.path.join(settings.MEDIA_ROOT, subPath)
    if not os.path.isdir(FilePath):
        os.makedirs(FilePath)
    # * file name encode
    m = hashlib.md5()
    m.update(str(timezone.now()).encode())
    filename = "{}.{}".format(m.hexdigest(), ext)
    with open(os.path.join(FilePath, filename), 'wb') as f:
        for i in file.chunks():
            f.write(i)
        # * store relative  path in database
        return os.path.join(subPath, filename)


class pictureManager(models.Manager):
    def uploadImg(self, imageFile, alt="picture.alt",**extra_fields):
        # * create Picture Object
        filePath = upload_picture(imageFile)
        PictureObject = self.model(img_url=filePath,alt=alt)
        PictureObject.save()
        return PictureObject
