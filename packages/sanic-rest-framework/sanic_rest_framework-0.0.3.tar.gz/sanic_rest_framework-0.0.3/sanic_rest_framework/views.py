"""
@Author: WangYuXiang
@E-mile: Hill@3io.cc
@CreateTime: 2021/1/19 15:44
@DependencyLibrary:
@MainFunction：
@FileDoc:
    views.py
    基础视图文件
"""
import inspect

from sanic.log import logger
from sanic.response import json
from sanic_rest_framework.constant import ALL_METHOD
from sanic_rest_framework.exceptions import APIException, ValidationError
from sanic_rest_framework.filters import SearchFilter
from sanic_rest_framework.paginations import GeneralPagination
from sanic_rest_framework.status import RuleStatus, HttpStatus
from simplejson import dumps
from tortoise.queryset import QuerySet


class BaseAPIView:
    """基础API视图"""
    authentication_classes = ()
    permission_classes = ()

    async def dispatch(self, request, *args, **kwargs):
        """分发路由"""
        request.user = None
        method = request.method
        if method not in self.licensed_methods:
            return self.json_response(msg='发生错误：未找到%s方法' % method, status=RuleStatus.STATUS_0_FAIL,
                                      http_status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)
        handler = getattr(self, method.lower(), None)

        try:
            self.initial(request, *args, **kwargs)
            response = handler(request, *args, **kwargs)
            if inspect.isawaitable(request):
                request = await request
        except APIException as exc:
            response = self.handle_exception(exc)
        except ValidationError as exc:
            response = self.error_json_response(exc.message_dict, '数据验证失败')
        except AssertionError as exc:
            raise exc
        except Exception as exc:
            logger.error('--捕获未知错误--', exc)
            response = self.handle_uncaught_exception(exc)
        return response

    @classmethod
    def as_view(cls, methods=None, *class_args, **class_kwargs):

        # 许可的方法
        if methods is None:
            methods = ALL_METHOD

        # 返回的响应方法闭包
        def view(request, *args, **kwargs):
            self = view.base_class(*class_args, **class_kwargs)
            self.licensed_methods = methods
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        view.base_class = cls
        view.API_DOC_CONFIG = class_kwargs.get('API_DOC_CONFIG')  # 未来的API文档配置属性+
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__name__ = cls.__name__
        return view

    def handle_exception(self, exc: APIException):
        return self.json_response(**exc.response_data())

    def handle_uncaught_exception(self, exc):
        """处理未知错误"""
        message = '{}:{}'.format(exc.__class__.__name__, '|'.join(exc.args))
        return self.json_response(msg=message, status=RuleStatus.STATUS_0_FAIL,
                                  http_status=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR)

    def json_response(self, data=None, msg="OK", status=RuleStatus.STATUS_1_SUCCESS,
                      http_status=HttpStatus.HTTP_200_OK):
        """
        Json 相应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :param status: 前台约定状态，供前台判断是否成功
        :param http_status: Http响应数据
        :return:
        """
        if data is None:
            data = {}
        response_body = {
            'data': data,
            'message': msg,
            'status': status
        }
        return json(body=response_body, status=http_status, dumps=dumps)

    def success_json_response(self, data=None, msg="Success", **kwargs):
        """
        快捷的成功的json响应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :return: json
        """
        status = kwargs.pop('status', RuleStatus.STATUS_1_SUCCESS)
        http_status = kwargs.pop('http_status', HttpStatus.HTTP_200_OK)
        return self.json_response(data=data, msg=msg, status=status, http_status=http_status)

    def error_json_response(self, data=None, msg="Fail", **kwargs):
        """
        快捷的失败的json响应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :return: json
        """
        status = kwargs.pop('status', RuleStatus.STATUS_0_FAIL)
        http_status = kwargs.pop('http_status', HttpStatus.HTTP_400_BAD_REQUEST)
        return self.json_response(data=data, msg=msg, status=status, http_status=http_status)

    async def get_object(self):
        """
        返回视图显示的对象。
        如果您需要提供非标准的内容，则可能要覆盖此设置
        queryset查找。
        """
        queryset = self.filter_queryset(self.get_queryset())

        lookup_field = self.lookup_field

        assert lookup_field in self.kwargs, (
                '%s 不存在于 %s 的 Url配置中的关键词内 ' %
                (lookup_field, self.__class__.__name__,)
        )

        filter_kwargs = {lookup_field: self.kwargs[lookup_field]}
        obj = await queryset.get_or_none(**filter_kwargs)
        if obj is None:
            raise APIException('不存在%s为%s的数据' % (lookup_field, self.kwargs[lookup_field]), http_status=HttpStatus.HTTP_200_OK)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_authenticators(self):
        """
        实例化并返回此视图可以使用的身份验证器列表
        """
        return [auth() for auth in self.authentication_classes]

    def check_authentication(self, request):
        """
        检查权限 查看是否拥有权限，并在此处为Request.User 赋值
        :param request: 请求
        :return:
        """
        for authenticators in self.get_authenticators():
            request.user = authenticators.authenticate(request, request.user)

    def get_permissions(self):
        """
        实例化并返回此视图所需的权限列表
        """
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        """
        检查是否应允许该请求，如果不允许该请求，
        则在 has_permission 中引发一个适当的异常。
        :param request: 当前请求
        :return:
        """
        for permission in self.get_permissions():
            permission.has_permission(request, self)

    def check_object_permissions(self, request, obj):
        """
        检查是否应允许给定对象的请求, 如果不允许该请求，
        则在 has_object_permission 中引发一个适当的异常。
            常用于 get_object() 方法
        :param request: 当前请求
        :param obj: 需要鉴权的模型对象
        :return:
        """
        for permission in self.get_permissions():
            permission.has_object_permission(request, self, obj)

    def check_throttles(self, request):
        """
        检查范围频率。
        则引发一个 APIException 异常。
        :param request:
        :return:
        """
        pass

    def initial(self, request, *args, **kwargs):
        """
        在请求分发之前执行初始化操作，用于检查权限及检查基础内容
        """
        self.check_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)


class APIView(BaseAPIView):
    queryset = None
    lookup_field = 'pk'
    serializer_class = None
    pagination_class = None
    filter_class = SearchFilter
    search_fields = None

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s'应该包含一个'queryset'属性，"
                "或重写`get_queryset()`方法。"
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def filter_queryset(self, queryset):
        return self.filter_class().filter_queryset(self.request, queryset, self)

    def get_serializer(self, *args, **kwargs):
        """
        返回应该用于验证和验证的序列化程序实例
        对输入进行反序列化，并对输出进行序列化。
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        返回用于序列化器的类。
        默认使用`self.serializer_class`。

        如果您需要提供其他信息，则可能要覆盖此设置
        序列化取决于传入的请求。

        （例如，管理员获得完整的序列化，其他获得基本的序列化）
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )
        return self.serializer_class

    def get_serializer_context(self):
        """
        提供给序列化程序类的额外上下文。
        """
        return {
            'request': self.request,
            'view': self
        }

    @property
    def paginator(self):
        """
        与视图关联的分页器实例，或“None”。
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    async def paginate_queryset(self, queryset):
        """
        返回单页结果，如果禁用了分页，则返回“无”。
        """
        if self.paginator is None:
            return None
        return await self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        返回给定输出数据的分页样式`Response`对象。
        """
        assert self.paginator is not None
        return self.paginator.response(self.request, data)


class ListModelMixin:
    """
    适用于输出列表类型数据
    """
    pagination_class = GeneralPagination
    detail = False

    async def get(self, request, *args, **kwargs):
        return await self.list(request, *args, **kwargs)

    async def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = await self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(await serializer.data)
            return self.success_json_response(data=data)

        serializer = self.get_serializer(queryset, many=True)
        return self.success_json_response(data=await serializer.data)


class CreateModelMixin:
    """
    适用于快速创建内容
    占用 post 方法
    """

    async def post(self, request, *args, **kwargs):
        return await self.create(request, *args, **kwargs)

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await serializer.is_valid(raise_exception=True)
        await self.perform_create(serializer)
        return self.success_json_response(data=await serializer.data, http_status=HttpStatus.HTTP_201_CREATED)

    async def perform_create(self, serializer):
        await serializer.save()


class DetailModelMixin:
    """
    适用于查询指定PK的内容
    """
    detail = True

    async def get(self, request, *args, **kwargs):
        return await self.detail(request, *args, **kwargs)

    async def detail(self, request, *args, **kwargs):
        instance = await self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_json_response(data=await serializer.data)


class UpdateModelMixin:
    """
    适用于快速创建更新操作
    """

    async def put(self, request, *args, **kwargs):
        return await self.update(request, *args, **kwargs)

    async def patch(self, request, *args, **kwargs):
        return await self.partial_update(request, *args, **kwargs)

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = await self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        await serializer.is_valid(raise_exception=True)
        await self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
        #     instance._prefetched_objects_cache = {}

        return self.success_json_response(data=await serializer.data)

    async def perform_update(self, serializer):
        await serializer.save()

    async def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return await self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    用于快速删除
    """

    async def delete(self, request, *args, **kwargs):
        return await self.destroy(request, *args, **kwargs)

    async def destroy(self, request, *args, **kwargs):
        instance = await self.get_object()
        await self.perform_destroy(instance)
        return self.success_json_response(status=HttpStatus.HTTP_204_NO_CONTENT)

    async def perform_destroy(self, instance):
        await instance.delete()
