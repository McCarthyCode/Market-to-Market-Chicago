from datetime import datetime

from django.shortcuts import render, redirect, reverse
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Album, Image
from .forms import UpdateAlbumTitleForm, AddImagesForm
from mtm.settings import TZ, NAME

def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Album.objects.create_album(request)

    if not valid:
        for error in response:
            messages.error(request, error)
    else:
        messages.success(request, response, extra_tags='safe')

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

    update_album_title = UpdateAlbumTitleForm()
    add_images = AddImagesForm()

    return render(request, 'images/album.html', {
        **response,
        'update_album_title': update_album_title,
        'add_images': add_images,
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

# def update_album_title(request):
#     if request.method == 'POST':
#         form = UpdateAlbumTitleForm(request.POST)

#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'name.html', {'form': form})
