from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from mtm.settings import TZ, NAME

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/index.html', {
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def category(request, category):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/index.html', {
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
