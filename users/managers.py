from __future__ import unicode_literals

import re
import pytz
from datetime import datetime, timedelta

from django.db.models import Manager
from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password
from mtm.settings import TIME_ZONE
from users import models

TZ = pytz.timezone(TIME_ZONE)
NAME = 'Market to Market Chicago'
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&’*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$')

class ProfileManager(Manager):
    def index(self, request):
        profile = models.Profile.objects.get(user__pk=request.session['id']) \
            if 'id' in request.session else None

        # if profile != None:
        #     return {
        #         'profile': profile,
        #         'name': NAME,
        #         'year': datetime.now(TZ).year,
        #     }

        return {
            'profile': profile,
            'name': NAME,
            'year': datetime.now(TZ).year,
        }


    def login_register(self, request, action):
        errors = []

        """
        Validate user input
        """
        # # checks if user is registering
        # if action == 'register':
        #     if len(request.POST['first-name']) == 0 or \
        #         len(request.POST['last-name']) == 0:
        #         errors.append('Please enter your first and last name.')
        #     if len(request.POST['email']) == 0:
        #         errors.append('Please enter your email.')
        #     elif not EMAIL_REGEX.match(request.POST['email']):
        #         errors.append('Please enter a valid email.')
        #     if len(request.POST['phone']) == 0:
        #         errors.append('Please enter your phone number.')
        #     if len(request.POST['password']) < 8:
        #         errors.append(
        #             'Please enter a password that contains at least 8 characters.')
        #     if request.POST['confirm-password'] != request.POST['password']:
        #         errors.append('Passwords must match.')
        # # checks if user is logging in
        # elif action == 'login':
        #     if not EMAIL_REGEX.match(request.POST['email']):
        #         errors.append('Please enter a valid email.')

        """
        Login/Register
        """
        if not errors:
            # checks if username exists in database and
            # stores any User associated with it
            try:
                user = User.objects.get(username=request.POST['username'])
            except User.DoesNotExist:
                user = None
            username_exists = user != None

            # checks if user is registering
            if action == 'register':
                # checks if registering user email already exists
                if username_exists:
                    errors.append(
                        'A user account with this username already exists.')
                    return (False, errors)

                # otherwise bcrypt password and create user
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    first_name=request.POST['first-name'],
                    last_name=request.POST['last-name'],
                )
                models.Profile.objects.create(
                    user=user,
                )

                return (True, user.id)

            elif action == 'login':
                # compares user password with posted password
                if username_exists:
                    correct_pw = user.check_password(
                        request.POST['password'])
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

            else:
                errors.append('Invalid action.')

        return (False, errors)
