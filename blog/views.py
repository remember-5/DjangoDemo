from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from blog.serializers import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ArticleInfoView(ModelViewSet):
    queryset = BlogArticle.objects.all()  # 获取查询结果集
    serializer_class = ArticleSerializer  # 指定序列化器
