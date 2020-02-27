from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('people/', views.people, name='people'),
    path('news-feed/', views.news_feed, name='news-feed'),
    re_path(r'^(?P<slug>(nightlife|restaurants|nightlife-restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit))/$', views.category, name='category'),
]
