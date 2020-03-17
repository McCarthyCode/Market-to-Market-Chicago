from django.urls import path, re_path

from . import views
from mtm.settings import DEBUG

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('people-to-know/', views.people, name='people-to-know'),
    path('create-person/', views.create_person, name='create-person'),
    re_path(r'update-person/(?P<person_id>[1-9]\d*)/', views.update_person, name='update-person'),
    re_path(r'delete-person/(?P<person_id>[1-9]\d*)/', views.delete_person, name='delete-person'),
    path('news-feed/', views.news_feed, name='news-feed'),
    re_path(r'^(?P<slug>(nightlife|restaurants|nightlife-restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit))/$', views.category, name='category'),
]

if DEBUG:
    urlpatterns += [
        re_path(r'^404/', views.handler404),
        re_path(r'^500/', views.handler500),
    ]