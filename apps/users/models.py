'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-16 16:34:41
LastEditors: zpliu
LastEditTime: 2022-07-06 16:38:38
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
from django.contrib.auth import get_user_model

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
        (0, 'Teacher'),
        (1, 'Post doctor'),
        (2, 'PhD student'),
        (3, 'Master Student'),
        (4, 'Visiting Scholar'),
    )
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=30, blank=False, default="None")
    sex = models.IntegerField(choices=sex_choise, blank=True, null=0,default=0)
    img_url = models.ManyToManyField(
        customer_picture, through="UserPicture", through_fields=('user', 'img'),)
    people_type = models.IntegerField(
        choices=peopleType, blank=True, null=0,default=4, verbose_name="人员类别")
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
        PictureObject = self.img_url.all().filter(alt="avatar").first()
        if PictureObject:
            imgURL = "{}{}".format(
                settings.WEB_URL, PictureObject.img_url)
        else:
            imgURL = ""
        return imgURL

    @property
    def info(self):
        '''获取用户的详细信息
        '''
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'sex': self.get_sex_display(),  # choise
            'jobTitle': self.jobTitle,
            'peopleType': self.get_people_type_display(),
            'recruit': self.recruit,
            'contact': self.contact,
            'office_site': self.office_site,
            'teacher': self.teacher,
            'imageURL': self.avatar
        }
    @property
    def teacher_nickname(self):
        userObject=get_user_model()
        teacherInstance=userObject.objects.filter(id=self.teacher).first()
        if teacherInstance:
            return teacherInstance.name
        else:
            return "暂无信息"
class UserPicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ForeignKey(customer_picture, on_delete=models.CASCADE)
    # *other field
    pubshedDate = models.DateTimeField(default=timezone.now)
    objects = user_picture_relationship_Manager()

    class Meta:
        db_table = "user_img_relationship"
