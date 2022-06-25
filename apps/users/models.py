'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 16:34:41
LastEditors: zpliu
LastEditTime: 2022-06-24 10:50:38
@param: 
'''


from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from pymysql import NULL
from .managers import CustomUserManager, user_picture_relationship_Manager
from django.utils.translation import gettext_lazy as _
from picture.models import customer_picture
import django.utils.timezone as timezone


class User(AbstractBaseUser, PermissionsMixin):
    '''
    #* email primary key
    #* username
    '''
    sex_choise = (
        (0, "男"),
        (1, "女"),
    )
    peopleType = (
        (0, '老师'),
        (1, '博士后'),
        (2, '博士'),
        (3, '硕士'),
        (4, '访问学者'),
    )
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=30, blank=False, default="None")
    sex = models.IntegerField(choices=sex_choise, blank=True, null=NULL)
    img_url = models.ManyToManyField(
        customer_picture, through="UserPicture", through_fields=('user', 'img'),)
    people_type = models.IntegerField(
        choices=peopleType, blank=True, null=NULL)
    contact = models.CharField(max_length=50, blank=True, null=NULL)
    office_site = models.CharField(max_length=100, blank=True, null=NULL)
    info_detail = models.TextField(
        blank=True, null=NULL, default='[{"tagName":"基本信息","vHtml":"<p></p>"}]')
    jobTitle = models.CharField(max_length=100, blank=True, null=NULL)
    teacher = models.IntegerField(blank=True, null=NULL)
    recruit = models.CharField(max_length=100, blank=True, null=NULL)
    # info_detail = models.JSONField(null=True,blank=True,)
    is_active = models.BooleanField(default=True)  # 账号是否处于激活状态，否则不能登录
    # * unique validate field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def check_is_superuser(self):
        return self.is_superuser
    
    @property
    def avatar(self):
        '''get absoulate router 
        '''
        PictureObject=self.img_url.all().first()
        if PictureObject:
            imgURL = "{}{}".format(
                settings.WEB_URL, PictureObject.img_url)
        else:
            imgURL = ""
        return imgURL



class UserPicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ForeignKey(customer_picture, on_delete=models.CASCADE)
    # *other field
    pubshedDate = models.DateTimeField(default=timezone.now)
    objects = user_picture_relationship_Manager()

    class Meta:
        db_table = "user_img_relationship"
