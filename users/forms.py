from django import forms
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

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
