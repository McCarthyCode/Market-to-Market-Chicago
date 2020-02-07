from django.urls import path, re_path

from . import views

urlpatterns = [
    path('neighborhoods/autocomplete/', views.neighborhood_autocomplete, name='neighborhood-autocomplete'),
    re_path(r'^neighborhoods/(?P<slug>[a-z]+(-[a-z]+)*)/(?P<neighborhood_id>[1-9]\d*)/$', views.neighborhood, name='neighborhood'),
    path('locations/autocomplete/', views.location_autocomplete, name='location-autocomplete'),
    path('locations/update/', views.update_location, name='update'),
    re_path(r'^(?P<category_slug>(nightlife|restaurants|arts-and-entertainment|health-and-fitness|sports|non-profit|misc))/(?P<location_slug>[\da-z]+(-[\da-z]+)*)/(?P<location_id>[1-9]\d*)/$', views.location, name='location'),
]
