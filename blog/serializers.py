from rest_framework import serializers
from blog.models import *


# 定义序列化程序
class ArticleSerializer(serializers.ModelSerializer):
    """
    指定需要序列化的模型和字段
    """
    class Meta:
        model = BlogArticle  # 数据库表名
        fields = '__all__'  # 所有的字段都要序列化模型格式:
