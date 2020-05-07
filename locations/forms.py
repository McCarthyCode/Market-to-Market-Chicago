from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Location, Neighborhood
from mtm.settings import URL_REGEX, HTTP_HTTPS_REGEX, PHONE_REGEX

class LocationForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name',
            'autocomplete': 'off',
        }),
    )
    category = forms.ChoiceField(
        label='Category',
        choices=Location.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control col-12 col-md-6',
            'autocomplete': 'off',
        }),
    )
    neighborhood_id = forms.CharField(
        label='',
        widget=forms.HiddenInput(attrs={
            'value': '0',
            'autocomplete': 'off',
        }),
    )
    neighborhood = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Neighborhood (enter name to search for existing or to create new)',
            'autocomplete': 'off',
        }),
    )
    address1 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address',
            'autocomplete': 'off',
        }),
    )
    address2 = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
        }),
    )
    city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-12 col-md-6',
            'placeholder': 'City',
            'value': 'Chicago',
            'autocomplete': 'off',
        }),
    )
    state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-6 col-md-3',
            'placeholder': 'State',
            'value': 'IL',
            'autocomplete': 'off',
        }),
    )
    zip_code = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-6 col-md-3',
            'placeholder': 'Zip Code (optional)',
            'autocomplete': 'off',
        }),
    )
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-12',
            'placeholder': 'Website (optional)',
            'autocomplete': 'off',
        }),
    )
    phone = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-12',
            'placeholder': 'Phone (optional)',
            'autocomplete': 'off',
        }),
    )
    no_kitchen = forms.BooleanField(
        required=False,
        label='Outside Food Allowed',
        widget=forms.CheckboxInput(attrs={
            'autocomplete': 'off',
        }),
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        cleaned_data['category'] = int(cleaned_data['category'])

        try:
            cleaned_data['neighborhood'] = \
                Neighborhood.objects.get(id=cleaned_data['neighborhood_id'])
        except Neighborhood.DoesNotExist:
            cleaned_data['neighborhood'] = \
                Neighborhood.objects.create_neighborhood(cleaned_data['neighborhood'])

        if cleaned_data['website'] and not URL_REGEX.match(cleaned_data['website']):
            if HTTP_HTTPS_REGEX.match(cleaned_data['website']):
                raise forms.ValidationError('Please enter a valid URL.')
            else:
                raise forms.ValidationError(
                    'Please enter a valid URL.',
                    'URL must start with http:// or https://.',
                )

        if cleaned_data['phone']:
            cleaned_data['phone'] = PHONE_REGEX.sub(r'\2\3\4', cleaned_data['phone'])

        if cleaned_data['no_kitchen']:
            if int(cleaned_data['category']) == 0:
                cleaned_data['category'] = 2
            elif int(cleaned_data['category']) != 2:
                cleaned_data['no_kitchen'] = False

        return cleaned_data

    class Meta:
        model = Location
        fields = [
            'name',
            'category',
            'neighborhood',
            'address1',
            'address2',
            'city',
            'state',
            'zip_code',
            'website',
            'phone',
            'no_kitchen',
        ]
