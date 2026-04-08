from django.urls import re_path, include, path
from snippets import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# 添加文档视图
schema_view = get_schema_view(
    openapi.Info(
        title="Pastebin API",
        default_version="v1",
        description="API for pasting code snippets",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 路由器注册视图
router = DefaultRouter()
router.register(r"snippets", views.SnippetViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
    path(
        r"swagger(<format>\.json|\.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        r"swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# 登陆与注销视图
urlpatterns += [
    re_path(r"^api-auth/", include("rest_framework.urls")),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
