from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# 定义视图处理的路由器
# router = DefaultRouter()
# router.register('article', views.ArticleInfoView)  # 在路由器中注册视图集

urlpatterns = [
    path('', views.index, name='index'),
    path('user_post', views.user_post, name='user-post'),
    path('user_like', views.user_like, name='user-like'),
    path('challenge', views.challenge, name='challenge'),
    path('music', views.music, name='music'),
]

# urlpatterns += router.urls
