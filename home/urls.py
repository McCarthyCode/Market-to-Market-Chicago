from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<category>(nightlife|restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit|misc))/$', views.category, name='category'),
]
