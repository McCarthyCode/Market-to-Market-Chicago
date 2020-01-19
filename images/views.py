from datetime import datetime

from django.shortcuts import render, redirect, reverse
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Album
from mtm.settings import TZ, NAME

def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Album.objects.create_album(request)

    if not valid:
        for error in response:
            messages.error(request, error)
    else:
        messages.success(request, response)

    return redirect('users:index')

def album(request, album_title, album_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    valid, response = Album.objects.album(album_title, album_id)

    if not valid:
        def invalid_id():
            messages.error(request, response['error'])

            return redirect('users:index')

        def invalid_slug():
            return HttpResponseRedirect(
                reverse('images:album', args=response['args']))

        actions = {
            'invalid ID': invalid_id,
            'invalid slug': invalid_slug,
        }

        return actions[response['status']]()

    return render(request, 'images/album.html', {
        **response,
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
