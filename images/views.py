from django.shortcuts import render, redirect
from django.http import (
    HttpResponseBadRequest,
    # HttpResponseNotFound,
    # HttpResponseRedirect,
    # JsonResponse,
)
from django.contrib import messages

from .models import Album

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
