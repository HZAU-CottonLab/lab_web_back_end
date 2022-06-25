'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-25 16:49:21
LastEditors: zpliu
LastEditTime: 2022-06-25 20:26:18
@param: 
'''
from django.db import models
from datetime import datetime

class publicationManage(models.Manager):
    def create(self,title,author,periodical,date,doi,**extra_fields):
        publicationInstance=self.model(
            title=title,
            author=author,
            periodical=periodical,
            date=date,
            doi=doi,
        )
        publicationInstance.save()
        return publicationInstance



# Create your models here.
class publication(models.Model):
    title = models.TextField(blank=False)
    date = models.DateField()
    author = models.TextField(blank=False)
    periodical = models.TextField(blank=False)
    doi = models.TextField(blank=False)
    objects=publicationManage()
    @property
    def data(self):
        return {
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'periodical':self.periodical,
            'doi':self.doi,
            'date':datetime.strftime(self.date,'%Y-%m-%d'),

        }
    @property        
    def year(self):
        return datetime.strftime(self.date,'%Y')

