import pytz

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from mtm.settings import TIME_ZONE
from users.models import Profile

NAME = 'Market to Market Chicago'

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    profile = Profile.objects.get(user__pk=request.session['id']) \
        if 'id' in request.session else None

    return render(request, 'home/index.html', {
        'profile': profile,
        'name': NAME,
        'year': datetime.now(pytz.timezone(TIME_ZONE)).year,
    })
