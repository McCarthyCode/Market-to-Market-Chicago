from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect

from .models import Invite
from events.models import Event

from .forms import CreateInvitesForm, RegistrationForm
from locations.forms import CreateLocationForm
from articles.forms import CreateArticleForm

from mtm.settings import NAME, TZ, MAX_INVITES

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    if request.user.is_superuser:
        return render(request, 'users/index.html', {
            'create_article_form': CreateArticleForm(),
            'create_invites_form': CreateInvitesForm(),
            'invites': [x for x in Invite.objects.filter(sent=False).order_by('date_created') if not x.expired][:MAX_INVITES],
            'create_location_form': CreateLocationForm(),
            'user': request.user,
            'name': NAME,
            'year': datetime.now(TZ).year,
        })

    return render(request, 'users/index.html', {
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
    if request.method != 'POST' or not request.user.is_superuser:
        return HttpResponseBadRequest()

    form = CreateInvitesForm(request.POST)

    if form.is_valid():
        qty = form.cleaned_data['qty']

        for i in range(qty):
            invite = Invite.create()

        messages.success(request, 'You have successfully created %d invite%s.' % (qty, '' if qty == 1 else 's'))
    else:
        for reference, message in form.errors.items():
            if reference == '__all__':
                error = message.as_text().replace('* ', '')
                messages.error(request, error)
                break

    return redirect('users:index')

def invite(request, code):
    invite = Invite.get_invite_or_404(code)
    if invite.user or not invite.sent:
        raise Http404

    if request.method == 'GET':
        return render(request, 'users/invite.html', {
            'code': code,
            'form': RegistrationForm(),
            'name': NAME,
            'year': datetime.now(TZ).year,
        })
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            pass
        else:
            for reference, message in form.errors.items():
                if reference == '__all__':
                    error = message.as_text().replace('* ', '')
                    messages.error(request, error)
                    break

            return render(request, 'users/invite.html', {
                'code': code,
                'form': form,
                'name': NAME,
                'year': datetime.now(TZ).year,
            })
    else:
        return HttpResponseBadRequest()

    return redirect('users:index')

def mark_invite_sent(request, code):
    if request.method != 'GET' or not request.user.is_superuser:
        return HttpResponseBadRequest()

    invite = Invite.get_invite_or_404(code)
    invite.sent = True
    invite.save()

    messages.success(request, 'Invite #%d successfully marked as sent.' % invite.id)

    return redirect('users:index')

def delete_invite(request, code):
    if request.method != 'GET' or not request.user.is_superuser:
        return HttpResponseBadRequest()

    invite = Invite.get_invite_or_404(code)
    invite_id = invite.id
    invite.delete()

    messages.success(request, 'Invite #%d successfully deleted.' % invite_id)

    return redirect('users:index')
