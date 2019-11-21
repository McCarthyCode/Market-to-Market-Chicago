from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from mtm.settings import TZ, NAME

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/index.html', {
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
