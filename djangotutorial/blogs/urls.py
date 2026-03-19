from . import views
from django.urls import path

app_name = "blogs"  # 设置命名空间
urlpatterns = [
    path("", views.index_page, name="index"),
    path("index", views.index_page, name="index"),
    path("article/<int:article_id>", views.blog_page, name="article_page"),
    path("tags/", views.tag_page, name="tag_index"),
]
