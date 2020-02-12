from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/$', views.article, name='article'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/update/$', views.update, name='update'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/delete/$', views.delete, name='delete'),
    path('by-page/', views.by_page, name='by-page'),
]
