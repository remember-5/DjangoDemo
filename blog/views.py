from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from blog.serializers import *
from django.db import connection

cursor = connection.cursor()


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def page(request):
    cursor.execute("select * from blog_article")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return HttpResponse(rows)


class ArticleInfoView(ModelViewSet):
    queryset = BlogArticle.objects.all()  # 获取查询结果集
    serializer_class = ArticleSerializer  # 指定序列化器
