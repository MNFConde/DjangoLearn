from django.urls import re_path, include, path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

# 路由器注册视图
router = DefaultRouter()
router.register(r"snippets", views.SnippetViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
]

# 登陆与注销视图
urlpatterns += [
    re_path(r"^api-auth/", include("rest_framework.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
