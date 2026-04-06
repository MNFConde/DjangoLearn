from django.urls import re_path, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r"^snippets/$", views.SnippetList.as_view()),
    re_path(r"^snippets/(?P<pk>[0-9]+)/$", views.SnippetDetail.as_view()),
    re_path(r"^user/$", views.UserList.as_view()),
    re_path(r"^user/(?P<pk>[0-9]+)/$", views.UserDetail.as_view()),
    re_path(r"^api-auth/", include("rest_framework.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
