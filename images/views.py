from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, reverse

from .models import Album, Image
from .forms import UpdateAlbumTitleForm, AddImagesForm
from mtm.settings import TZ, NAME

def create_album(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        response = Album.objects.create_album(request)
    except ValidationError as errors:
        for error in errors:
            messages.error(request, error)

        return redirect('users:index')

    messages.success(request, response['success'])

    return HttpResponseRedirect(
        reverse('images:album', args=response['args'])
    )

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
                reverse('images:album', args=response['args'])
            )

        actions = {
            'invalid ID': invalid_id,
            'invalid slug': invalid_slug,
        }

        return actions[response['status']]()

    update_album_title = UpdateAlbumTitleForm()
    add_images = AddImagesForm()

    return render(request, 'images/album.html', {
        **response,
        'update_album_title': update_album_title,
        'add_images': add_images,
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def update_album_title(request, album_title, album_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        response = Album.objects.update_title(request, album_id)
    except ValidationError as errors:
        for error in errors:
            if error != 'The specified album could not be found.':
                messages.error(request, error)

        return HttpResponseRedirect(
            reverse('images:album', args=[album_title, album_id])
        )
    except PermissionDenied:
        return HttpResponseRedirect(
            reverse('images:album', args=[album_title, album_id])
        )

    messages.success(request, response['success'])

    return HttpResponseRedirect(
        reverse('images:album', args=response['args'])
    )

def add_images(request, album_title, album_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        response = Album.objects.add_images(request, album_id)
    except ValidationError as errors:
        for error in errors:
            messages.error(request, error)

        return HttpResponseRedirect(
            reverse('images:album', args=[album_title, album_id])
        )
    except PermissionDenied:
        return HttpResponseRedirect(
            reverse('images:album', args=[album_title, album_id])
        )

    messages.success(request, response['success'])

    return HttpResponseRedirect(
        reverse('images:album', args=response['args'])
    )

def remove_images(request, album_title, album_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        response = Album.objects.remove_images(request, album_id)
    except PermissionDenied:
        return HttpResponseRedirect(
            reverse('images:album', args=[album_title, album_id])
        )

    if response['success']:
        messages.success(request, response['success'])

    if response['errors']:
        for error in response['errors']:
            messages.error(request, error)

    return HttpResponseRedirect(
        reverse('images:album', args=[album_title, album_id])
    )

def delete_album(request, album_title, album_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        response = Album.objects.delete_album(request, album_id)
    except ValidationError as errors:
        for error in errors:
            messages.error(request, error)

        return redirect('users:index')
    except PermissionDenied:
        return HttpResponseRedirect(
            reverse('images:album', args=[album_title, album_id])
        )

    if response['success']:
        messages.success(request, response['success'])

    return redirect('users:index')

def album_autocomplete(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/autocomplete.html',
        Album.objects.autocomplete(request)
    )
