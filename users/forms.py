from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

from .validators import validate_password
from .models import Invite
from mtm.settings import MAX_INVITES

class CreateInvitesForm(forms.Form):
    qty = forms.IntegerField(
        label='Number of Invites',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(MAX_INVITES)
        ],
        widget=forms.NumberInput(attrs={
            'class': 'form-control col-12 col-md-6',
            'value': 1,
            'min': 1,
            'max': MAX_INVITES,
            'autocomplete': 'off',
        })
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        try:
            cleaned_data['qty'] = int(cleaned_data['qty'])
        except KeyError:
            raise forms.ValidationError(_('You have entered an invalid number of invites. Please enter a value between 1 and %d.' % MAX_INVITES), code='invalid')

        return cleaned_data

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'autocomplete': 'off',
        }),
    )
    password = forms.CharField(
        label='',
        validators=[
            validate_password,
        ],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'off',
        }),
    )
    password_confirm = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'autocomplete': 'off',
        }),
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        try:
            if cleaned_data['password'] != cleaned_data['password_confirm']:
                raise forms.ValidationError(_('Passwords must match.'), code='mismatch')
        except KeyError:
            pass

        return cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password']
