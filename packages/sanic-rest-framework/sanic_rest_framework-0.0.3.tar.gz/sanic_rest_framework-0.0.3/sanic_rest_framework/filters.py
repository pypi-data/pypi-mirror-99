"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/3/10 17:25
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    filters.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/3/10 17:25 change 'Fix bug'
        
"""
LOOKUP_SEP = '__'


class SimpleFilter:
    """简单过滤器"""

    def filter_queryset(self, request, queryset, view):
        raise NotImplementedError(".filter_queryset() must be overridden.")

    def construct_orm_filter(self, field_name, view, request):
        return ''


class SearchFilter(SimpleFilter):
    lookup_prefixes = {
        '^': 'istartswith',
        '$': 'iendswith',
        '>': 'gt',
        '<': 'lt',
        '>=': 'gte',
        '<=': 'lte',
        '=': 'contains',
        '@': 'icontains'
    }

    def get_search_fields(self, request, view):
        """
        搜索字段是从视图获取的，但请求始终是
        传递给此方法。子类可以重写此方法以
        根据请求内容动态更改搜索字段。
        """
        return getattr(view, 'search_fields', None)

    def filter_queryset(self, request, queryset, view):
        """
        根据定义的搜索字段过滤传入的queryset
        :param request: 当前请求
        :param queryset: 查询对象
        :param view: 当前视图
        :return:
        """
        search_fields = self.get_search_fields(request, view)
        if not search_fields:
            return queryset
        orm_filters = {}
        for search_field in search_fields:
            orm_filters.update(self.construct_orm_filter(search_field, request, view))
        return queryset.filter(**orm_filters)

    def dismantle_search_field(self, search_field):
        """
        拆解带有特殊字符的搜索字段
        :param search_field: 搜索字段
        :return: (field_name, lookup_suffix)
        """
        lookup_suffix_keys = list(self.lookup_prefixes.keys())
        lookup_suffix = None
        field_name = search_field
        for lookup_suffix_key in lookup_suffix_keys:
            if lookup_suffix_key in search_field:
                lookup_suffix = self.lookup_prefixes[lookup_suffix_key]
                field_name = search_field[len(lookup_suffix_key):]
                return field_name, lookup_suffix
        return field_name, lookup_suffix

    def construct_orm_filter(self, search_field, request, view):
        """
        构造适用于orm的过滤参数
        :param search_field: 搜索字段
        :param request: 当前请求
        :param view: 视图
        :return:
        """
        field_name, lookup_suffix = self.dismantle_search_field(search_field)
        args = request.args

        if field_name not in args:
            return {}
        if lookup_suffix:
            orm_lookup = LOOKUP_SEP.join([field_name, lookup_suffix])
        else:
            orm_lookup = field_name
        return {orm_lookup: self.get_filter_value(request, field_name)}

    def get_filter_value(self, request, field_name):
        """
        根据字段名从请求中得到值
        :param request: 当前请求
        :param field_name: 字段名
        :return:
        """
        values = request.args.get(field_name)
        return ''.join(values)
