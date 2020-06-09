from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# 定义视图处理的路由器
router = DefaultRouter()
router.register('article', views.ArticleInfoView)  # 在路由器中注册视图集

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += router.urls
