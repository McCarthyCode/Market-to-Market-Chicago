import pytz

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from mtm.settings import TIME_ZONE
from .models import Profile

NAME = 'Market to Market Chicago'

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'users/index.html', Profile.objects.index(request))


def login(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Profile.objects.login_register(request, 'login')

    if not valid:
        for error in response:
            messages.error(request, error)
        return redirect('users:index')

    profile = Profile.objects.get(pk=response)
    messages.success(request, 'Welcome back, %s!' % profile.user.first_name)
    request.session['id'] = response
    return redirect('users:index')


def logout(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    del request.session['id']
    messages.success(request, 'You have successfully signed out.')

    return redirect('users:index')
