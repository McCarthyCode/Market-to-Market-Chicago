from django.urls import path, re_path

from . import views

urlpatterns = [
    path('events/', views.index, name='index'),
    path('events/create/', views.create_event, name='create'),
    path('events/update/', views.update_event, name='update'),
    path('events/delete/', views.delete_event, name='delete'),
    path('events/month/', views.month, name='month'),
    path('events/by-date/', views.by_date, name='by-date'),
    path('events/by-location/', views.by_location, name='by-location'),
    path('events/prev/', views.prev, name='prev'),
    path('events/next/', views.next, name='next'),
    re_path(r'^(?P<category>(nightlife|restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit|misc))/(?P<location_name>[\da-z]+(-[\da-z]+)*)/(?P<event_name>[\da-z]+(-[\da-z]+)*)/(?P<event_id>[1-9]\d*)/$', views.event, name='event'),
]
