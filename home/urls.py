from django.urls import path, re_path

from . import views
from mtm.settings import STAGE

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('people-to-know/', views.people, name='people-to-know'),
    path('create-person/', views.create_person, name='create-person'),
    re_path(r'update-person/(?P<person_id>[1-9]\d*)/', views.update_person, name='update-person'),
    re_path(r'delete-person/(?P<person_id>[1-9]\d*)/', views.delete_person, name='delete-person'),
    path('create-contact/', views.create_contact, name='create-contact'),
    re_path(r'update-contact/(?P<contact_id>[1-9]\d*)/', views.update_contact, name='update-contact'),
    re_path(r'delete-contact/(?P<contact_id>[1-9]\d*)/', views.delete_contact, name='delete-contact'),
    path('news-feed/', views.news_feed, name='news-feed'),
    re_path(r'^(?P<slug>(nightlife|restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit|editorials-and-opinions))/$', views.category, name='category'),
    re_path(r'^(?P<slug>(nightlife|restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit|editorials-and-opinions))/(?P<page>[1-9]\d*)/$', views.category_feed, name='category-feed'),
]

if STAGE == 'development':
    urlpatterns += [
        re_path(r'^400/', views.handler400),
        re_path(r'^403/', views.handler403),
        re_path(r'^404/', views.handler404),
        re_path(r'^500/', views.handler500),
    ]
