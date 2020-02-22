from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('news-feed/', views.news_feed, name='news-feed'),
    re_path(r'^(?P<slug>(nightlife|restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit|misc))/$', views.category, name='category'),
]
