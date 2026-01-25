from . import views
from django.urls import path

app_name = 'polls'

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index_second, name="index_second"),
    path("specifics/<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]