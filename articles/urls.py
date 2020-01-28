from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    re_path(r'^(?P<article_title>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/$', views.article, name='article'),
]
