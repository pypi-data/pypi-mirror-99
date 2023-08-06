"""
@Author: WangYuXiang
@E-mile: Hill@3io.cc
@CreateTime: 2021/1/19 16:08
@DependencyLibrary: 无
@MainFunction：无
@FileDoc:
    routes.py
    便捷路由文件
"""
from typing import List, Type, Union

from sanic import Sanic, Blueprint

from .constant import ALL_METHOD, DETAIL_METHOD_GROUP, LIST_METHOD_GROUP


# 默认分组


class Route:
    def __init__(self):
        self.routes = []

    def register_route(self, prefix, viewset, name=None):
        """
        注册路由
        :param prefix: url 前缀
        :param viewset: 视图类
        :param name: 供 url_for 使用的名称
        :return:
        """
        if name is None:
            name = prefix

        dynamic_uri = '/{prefix}/<{lookup_field}:string>'
        static_uri = '/{prefix}'
        base_method_group = LIST_METHOD_GROUP
        if hasattr(viewset, 'detail') and viewset.detail:
            base_method_group = DETAIL_METHOD_GROUP

        viewset_methods = self.get_viewset_methods(viewset)
        viewset_dynamic_method = [i for i in viewset_methods if i in base_method_group['dynamic_method']]
        viewset_static_method = [i for i in viewset_methods if i in base_method_group['static_method']]

        if viewset_dynamic_method:
            self.routes.append({
                'handler': viewset.as_view(viewset_dynamic_method),
                'uri': dynamic_uri.format(prefix=prefix, lookup_field=viewset.lookup_field),
                'name': '{name}_detail'.format(name=name)
            })
        if viewset_static_method:
            self.routes.append({
                'handler': viewset.as_view(viewset_static_method),
                'uri': static_uri.format(prefix=prefix),
                'name': '{name}_list'.format(name=name)
            })

    def get_viewset_methods(self, viewset):
        """得到viewSet所有请求方法"""
        methods = []
        for method in ALL_METHOD:
            if hasattr(viewset, method.lower()):
                methods.append(method)
        return methods

    def initialize(self, destination: Union[Sanic, Blueprint]):
        """注册路由"""
        for route in self.routes:
            route['methods'] = ALL_METHOD
            destination.add_route(**route)
