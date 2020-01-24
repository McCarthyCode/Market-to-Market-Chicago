from datetime import datetime

from django.http import HttpResponseBadRequest
from django.shortcuts import render

from mtm.settings import TZ, NAME

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/index.html', {
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def category(request, category):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/index.html', {
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
