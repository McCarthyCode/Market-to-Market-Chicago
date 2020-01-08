from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User
from events.models import Event
from mtm.settings import NAME, TZ

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'users/index.html', {
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def process_login(request):
    # track errors as a list of strings
    errors = []

    # checks if username exists in database and
    # stores any User associated with it
    try:
        user = User.objects.get(username=request.POST['username'])
    except User.DoesNotExist:
        user = None
    username_exists = user != None

    # compares user password with posted password
    if username_exists:
        correct_pw = user.check_password(request.POST['password'])
    else:
        correct_pw = False

    if not correct_pw or not username_exists:
        errors.append(
            'The username and password combination you entered ' + \
            'does not exist in our database. Please register ' + \
            'or try again.')
        return (False, errors)

    # grabs user id to store in session in views
    if correct_pw:
        return (True, user.id)

    return (False, errors)

def login(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = process_login(request)

    if not valid:
        for error in response:
            messages.error(request, error)
        return redirect('users:index')

    user = User.objects.get(pk=response)
    if user.first_name:
        messages.success(request, 'Welcome back, %s!' % user.first_name)
    else:
        messages.success(request, 'Welcome back!')
    request.session['id'] = response
    return redirect('users:index')

def logout(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    del request.session['id']
    messages.success(request, 'You have successfully signed out.')

    return redirect('users:index')
