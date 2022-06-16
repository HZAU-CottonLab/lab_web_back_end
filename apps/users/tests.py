'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-14 17:50:28
LastEditors: zpliu
LastEditTime: 2022-06-16 20:20:00
@param: 
'''
from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='1944532210@qq.com',name="zpliu", password='f1oo')
        self.assertEqual(user.email, '1944532210@qq.com')
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")
