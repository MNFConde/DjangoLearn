from django.urls import re_path, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r"^$", views.api_root),
    re_path(r"^snippets/$", views.SnippetList.as_view(), name="snippet-list"),
    re_path(
        r"^snippets/(?P<pk>[0-9]+)/$",
        views.SnippetDetail.as_view(),
        name="snippet-detail",
    ),
    re_path(
        r"^snippets/(?P<pk>[0-9]+)/highlight/$",
        views.SnippetHighlight.as_view(),
        name="snippet-highlight",
    ),
    re_path(r"^user/$", views.UserList.as_view(), name="user-list"),
    re_path(r"^user/(?P<pk>[0-9]+)/$", views.UserDetail.as_view(), name="user-detail"),
]

# 登陆与注销视图
urlpatterns += [
    re_path(r"^api-auth/", include("rest_framework.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
