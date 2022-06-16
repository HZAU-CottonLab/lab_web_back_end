'''
Descripttion: 
version: 
Author: zpliu
Date: 2022-06-14 20:54:39
LastEditors: zpliu
LastEditTime: 2022-06-16 21:28:21
@param: 
'''
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, name,**extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,**extra_fields)
        # print(user.get_username())
        user.set_password(password)
        user.save()
        return user