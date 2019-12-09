from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add-event/', views.add_event, name='add_event'),
]
