from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.create_album, name='create'),
    path('autocomplete/', views.album_autocomplete, name='album-autocomplete'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<album_id>[1-9]\d*)/$', views.album, name='album'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<album_id>[1-9]\d*)/update/$', views.update, name='update'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<album_id>[1-9]\d*)/add/$', views.add_images, name='add'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<album_id>[1-9]\d*)/feed-toggle/$', views.feed_toggle, name='feed-toggle'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<album_id>[1-9]\d*)/delete-images/$', views.delete_images, name='delete-images'),
    re_path(r'^(?P<slug>[\da-z]+(-[\da-z]+)*)/(?P<album_id>[1-9]\d*)/delete-album/$', views.delete_album, name='delete-album'),
]
