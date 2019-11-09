import pytz

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from mtm.settings import TIME_ZONE

NAME = 'Market to Market Chicago'

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'users/index.html', {
        'name': NAME,
        'year': datetime.now(pytz.timezone(TIME_ZONE)).year,
    })
