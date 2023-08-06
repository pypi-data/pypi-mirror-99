"""
@Author: WangYuXiang
@E-mile: Hill@3io.cc
@CreateTime: 2021/1/19 15:45
@DependencyLibrary: 无
@MainFunction：无
@FileDoc:
    constant.py
    全局常量
"""
ALL_METHOD = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'}
DETAIL_METHOD_GROUP = {
    'dynamic_method': ['GET', 'PUT', 'DELETE', 'PATCH'],
    'static_method': ['POST', 'OPTION']
}
LIST_METHOD_GROUP = {
    'dynamic_method': ['PUT', 'DELETE', 'PATCH'],
    'static_method': ['GET', 'POST', 'OPTION']
}
