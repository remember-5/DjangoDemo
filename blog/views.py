# Create your views here.
import datetime
import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from blog.serializers import *
from django.db import connection

cursor = connection.cursor()


def index(request):
    return render(request, 'index.html')


def indexText(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def page(request):
    _page = request.GET.get("page")  # 第几页
    _limit = request.GET.get("limit")  # 每页多少
    if _page is None or _limit is None:  # 默认返回
        _page = 1
        _limit = 10
    cursor.execute("select * from blog_article")

    result = dictfetchall(cursor)
    cursor.close()

    paginator = Paginator(result, _limit)  # 转为限制行数的paginator对象
    total = paginator.count  # 计算总行数
    queryset = paginator.page(_page)  # 根据前端的页数选择对应的返回结果
    items = json.loads(json.dumps(list(queryset), cls=DateEncoder))
    # return JsonResponse(items)
    return HttpResponse(items, content_type="application/json,charset=utf-8")


class ArticleInfoView(ModelViewSet):
    queryset = BlogArticle.objects.all()  # 获取查询结果集
    serializer_class = ArticleSerializer  # 指定序列化器


# 服务于转换fetchall结果为列表嵌套字典
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]  # 拿到对应的字段列表
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        else:
            return json.JSONEncoder.default(self, obj)
