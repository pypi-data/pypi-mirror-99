"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/3/11 17:37
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    paginations.py
    分页器
@ChangeHistory:
    datetime action why
    example:
    2021/3/11 17:37 change 'Fix bug'
        
"""
from sanic.request import Request
from tortoise import Model

from sanic_rest_framework.exceptions import APIException
from sanic_rest_framework.status import HttpStatus
from sanic_rest_framework.utils import replace_query_param


class BasePagination:
    """抽象基类"""

    async def paginate_queryset(self, queryset, request, view):
        raise NotImplementedError(
            '必须在 `%s` 中实现异步的 `.paginate_queryset()` 方法' % self.__class__.__name__)

    def response(self, request, data):
        raise NotImplementedError(
            '必须在 `%s` 中实现 `.response()` 方法' % self.__class__.__name__)


class GeneralPagination(BasePagination):
    """通用分页器"""
    page_size = 60
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10000

    @property
    def count(self):
        assert hasattr(self, '_count'), '必须先执行 `.paginate_queryset()` 函数才能使用.count'
        return self._count

    def get_next_link(self, request: Request):
        assert hasattr(self, '_count'), '必须先执行 `.paginate_queryset()` 函数才能使用.get_next_link()'
        if self.page * self.page_size + self.page_size >= self.count:
            return None
        uri = request.server_path
        query_string = '?' + request.query_string
        query_string = replace_query_param(query_string, self.page_query_param, self.page + 1)
        query_string = replace_query_param(query_string, self.page_size_query_param, self.page_size)
        return uri + query_string

    def get_previous_link(self, request: Request):
        assert hasattr(self, '_count'), '必须先执行 `.paginate_queryset()` 函数才能使用.get_previous_link()'
        if self.page * self.page_size <= 0:
            return None
        uri = request.server_path
        query_string = '?' + request.query_string
        query_string = replace_query_param(query_string, self.page_query_param, self.page - 1)
        query_string = replace_query_param(query_string, self.page_size_query_param, self.page_size)
        return uri + query_string

    async def paginate_queryset(self, queryset, request, view):
        self.page = self.get_query_page(request)
        self.page_size = self.get_query_page_size(request)
        if not isinstance(queryset, Model):
            queryset = queryset.filter()
        self._count = await queryset.count()
        return queryset.limit(self.page_size).offset(self.page * self.page_size)

    def get_query_page(self, request):
        try:
            page = int(request.args.get(self.page_query_param, 0))
        except ValueError as exc:
            raise APIException('发生错误的分页数据', http_status=HttpStatus.HTTP_400_BAD_REQUEST)
        return page

    def get_query_page_size(self, request):
        try:
            page = int(request.args.get(self.page_size_query_param, self.page_size))
            if page > self.max_page_size:
                raise APIException('分页内容大小超出最大限制', http_status=HttpStatus.HTTP_400_BAD_REQUEST)
        except ValueError as exc:
            raise APIException('发生错误的分页数据', http_status=HttpStatus.HTTP_400_BAD_REQUEST)
        return page

    def response(self, request, data):
        return {
            'count': self.count,
            'next': self.get_next_link(request),
            'previous': self.get_previous_link(request),
            'results': data,
        }
