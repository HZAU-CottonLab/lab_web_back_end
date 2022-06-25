'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-20 14:11:08
LastEditors: zpliu
LastEditTime: 2022-06-24 10:50:09
@param: 
'''


from django.db import models
from pymysql import NULL
from .managers import pictureManager
from django.conf import settings
import os
# Create your models here.


class customer_picture(models.Model):
    img_url = models.ImageField(null=NULL, blank=True, upload_to="%Y/%y/%d")
    alt = models.CharField(blank=True, null=NULL,
                           max_length=100, default="picture.alt")
    objects = pictureManager()

    def __str__(self) -> str:
        return self.alt

    # @classmethod :无需实例化即可调用
    def delete(self):
        # * delete picture from disk and clear the record from database
        os.remove(os.path.join(settings.MEDIA_ROOT, str(self.img_url)))
        super(customer_picture, self).delete()

    @property
    def url(self):
        #拼接完整的访问路径
        imgURL = "{}{}".format(
            settings.WEB_URL, self.img_url)
        return imgURL
