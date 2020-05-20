from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^articles/create/$', views.create, name='create'),
    re_path(r'^articles/(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/$', views.article, name='article'),
    re_path(r'^articles/(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/update/$', views.update, name='update'),
    re_path(r'^articles/(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<article_id>[1-9]\d*)/delete/$', views.delete, name='delete'),
    re_path(r'^authors/create/$', views.create_author, name='create-author'),
    re_path(r'^authors/autocomplete/$', views.author_autocomplete, name='author-autocomplete'),
    re_path(r'^authors/(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<author_id>[1-9]\d*)/$', views.author, name='author'),
    re_path(r'^authors/(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<author_id>[1-9]\d*)/update/$', views.update_author, name='update-author'),
    re_path(r'^authors/(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<author_id>[1-9]\d*)/delete/$', views.delete_author, name='delete-author'),
]
