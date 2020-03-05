from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from .models import Invite
from events.models import Event

from .forms import CreateInvitesForm
from locations.forms import CreateLocationForm
from articles.forms import CreateArticleForm

from mtm.settings import NAME, TZ

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'users/index.html', {
        'create_invites_form': CreateInvitesForm(),
        'create_article_form': CreateArticleForm(),
        'create_location_form': CreateLocationForm(),
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def process_login(request):
    from django.contrib.auth import authenticate, login

    # track errors as a list of strings
    errors = []

    # checks if username and password combination exists in database
    user = authenticate(request,
        username=request.POST['username'],
        password=request.POST['password']
    )

    if not user:
        errors.append(
            'The username and password combination you entered ' + \
            'does not exist in our database. Please register ' + \
            'or try again.')

        return (False, errors)

    login(request, user)

    return (True, user)

def login(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = process_login(request)

    if not valid:
        for error in response:
            messages.error(request, error)

        return redirect('users:index')

    user = response
    if user.first_name:
        messages.success(request, 'Welcome back, %s!' % user.first_name)
    else:
        messages.success(request, 'Welcome back!')

    return redirect('users:index')

def logout(request):
    from django.contrib.auth import logout

    if request.method != 'GET':
        return HttpResponseBadRequest()

    logout(request)
    messages.success(request, 'You have successfully signed out.')

    return redirect('users:index')

def create_invites(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    form = CreateInvitesForm(request.POST)

    if form.is_valid():
        qty = form.cleaned_data['qty']

        for i in range(qty):
            invite = Invite.create()
            print(invite.link)

        messages.success(request, 'You have successfully created %d invite%s.' % (qty, '' if qty == 1 else 's'))
    else:
        for value, msg in form.errors.items():
            if value == '__all__':
                error = msg.as_text().replace('* ', '')
                messages.error(request, error)
                break

    return redirect('users:index')
