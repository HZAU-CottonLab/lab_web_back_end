'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 22:28:41
LastEditors: zpliu
LastEditTime: 2022-07-01 17:05:17
@param: 
'''
from pyexpat import model
from django.db import models
import django.utils.timezone as timezone
from datetime import datetime
# Create your models here.
from picture.models import customer_picture

class ResearchManger(models.Manager):
    def create(self,title,description,PictureObject,date,**extra_fields):
        researchObject=self.model(
            title=title,
            description=description,
            date=date,
            is_check=True
        )
        researchObject.save()
        #* save the relationship
        researchObject.imageURL.add(PictureObject)
        return researchObject 

class Research(models.Model):
    title=models.CharField(max_length=200,blank=False) 
    description=models.TextField(blank=False)
    date=models.DateField()
    imageURL=models.ManyToManyField(
        customer_picture,through='research_picture',through_fields=['research','img']
    )
    is_check=models.BooleanField(default=True,blank=False)
    objects=ResearchManger()
    @property
    def data(self):
        avatarObject=self.imageURL.all().filter(alt="avatar").first()
        if avatarObject:
            return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "date":datetime.strftime(self.date,'%Y-%m-%d'),
                "check":self.is_check,
                "imageURL":avatarObject.url,
            }

class research_picture(models.Model):
    research=models.ForeignKey(Research,on_delete=models.CASCADE)
    img=models.ForeignKey(customer_picture,on_delete=models.CASCADE)
    # *other field
    pubshedDate = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "research_img_relationship" 