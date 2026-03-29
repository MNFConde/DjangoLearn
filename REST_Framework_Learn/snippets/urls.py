from django.urls import re_path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r"^snippets/$", views.snippet_list),
    re_path(r"^snippets/(?P<pk>[0-9]+)/$", views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
