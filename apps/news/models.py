'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-24 09:21:40
LastEditors: zpliu
LastEditTime: 2022-06-24 15:06:50
@param: 
'''

from django.db import models
from pymysql import NULL
from picture.models import customer_picture
import django.utils.timezone as timezone
from datetime import datetime
# Create your models here.
class userManger(models.Manager):
    def news_add(self,title,description,vhtml,date,latest,check,PictureObject,**extra_fields):
        newsObject=self.model(
            title=title,
            description=description,
            vhtml=vhtml,
            date=date,
            latest=latest,
            check=check
        )
        newsObject.save()
        #* add picture relationship
        newsObject.imageURL.add(PictureObject)
        return newsObject

class News(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    vhtml = models.TextField(blank=False, null=NULL,default="<p></p>")
    date = models.DateField()
    latest = models.BooleanField(default=False, blank=False)
    check = models.BooleanField(default=True, blank=False)
    imageURL = models.ManyToManyField(
        customer_picture, through='newPicture', through_fields=('news', 'img'))
    objects=userManger()

    @property
    def data(self):
        avatarObject=self.imageURL.all().filter(alt="avatar").first()
        if avatarObject:
            return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "vhtml":self.vhtml,
                "date":datetime.strftime(self.date,'%Y-%m-%d'),
                "check":self.check,
                "imageURL":avatarObject.url,
                "latest":self.latest
            }
        else:
            return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "vhtml":self.vhtml,
                "date":datetime.strftime(self.date,'%Y-%m-%d'),
                "check":self.check,
                "imageURL":'',
                "latest":self.latest
            } 


class newPicture(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    img = models.ForeignKey(customer_picture, on_delete=models.CASCADE)
    # *other field
    pubshedDate = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "news_img_relationship"
