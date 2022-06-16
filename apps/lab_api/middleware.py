'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-10-17 21:09:23
LastEditors: zpliu
LastEditTime: 2021-10-17 21:42:40
@param: 
'''
from django.utils.deprecation import MiddlewareMixin 


class CommonMiddleware(MiddlewareMixin):
    '''404 validation
    '''
    def process_request(self,request):
        print("Md2处理请求：")

    def process_response(self,request,response):
        if response.status_code == 404:
            return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        print("Md2在执行%s视图前" %view_func.__name__)

    def process_exception(self,request,exception):
        print("Md2处理视图异常...")

