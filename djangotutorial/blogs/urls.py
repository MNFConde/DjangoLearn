from . import views
from django.urls import path

urlpatterns = [
    path("", views.index_page, name="index"),
    path("index", views.index_page, name="index"),
]
