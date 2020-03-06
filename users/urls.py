from django.urls import path, re_path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('invite/create/', views.create_invites, name='create-invites'),
    re_path(r'^invite/(?P<code>[\da-f]{32})/$', views.invite, name='invite'),
    re_path(r'^invite/(?P<code>[\da-f]{32})/mark-sent/$', views.mark_invite_sent, name='mark-sent'),
    re_path(r'^invite/(?P<code>[\da-f]{32})/delete/$', views.delete_invite, name='delete-invite'),
]
