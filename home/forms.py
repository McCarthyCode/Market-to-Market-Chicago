from django import forms
from django.utils.translation import gettext as _

from images.models import Person, Contact

from mtm.settings import PHONE_REGEX

class PersonForm(forms.ModelForm):
    prefix = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prefix (optional, e.g. Dr., Mr., Ms., etc.)',
            'autocomplete': 'off',
            'maxlength': 5,
        }),
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'autocomplete': 'off',
            'maxlength': 35,
        }),
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'autocomplete': 'off',
            'maxlength': 35,
        }),
    )
    suffix = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Suffix (optional, e.g. Jr., IV, M.D., etc.)',
            'autocomplete': 'off',
            'maxlength': 5,
        }),
    )
    image = forms.ImageField(
        required=False,
        label='Profile Image',
        widget=forms.FileInput(attrs={
            'class': 'col-12 col-md-8',
            'autocomplete': 'off',
        }),
    )
    clear_image = forms.BooleanField(
        required=False,
        label='Clear Existing Image',
    )
    bio = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Bio',
            'autocomplete': 'off',
        }),
    )
    phone = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone (optional)',
            'autocomplete': 'off',
        }),
    )
    email = forms.EmailField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email (optional)',
            'autocomplete': 'off',
        }),
    )
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Website (optional)',
            'autocomplete': 'off',
        }),
    )
    facebook = forms.CharField(
        required=False,
        label='facebook.com/',
        widget=forms.TextInput(attrs={
            'class': 'col-12 col-md-6 form-control',
            'placeholder': '(optional)',
            'autocomplete': 'off',
        }),
    )
    twitter = forms.CharField(
        required=False,
        label='twitter.com/',
        widget=forms.TextInput(attrs={
            'class': 'col-12 col-md-6 form-control',
            'placeholder': '(optional)',
            'autocomplete': 'off',
        }),
    )
    instagram = forms.CharField(
        required=False,
        label='instagram.com/',
        widget=forms.TextInput(attrs={
            'class': 'col-12 col-md-6 form-control',
            'placeholder': '(optional)',
            'autocomplete': 'off',
        }),
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        if cleaned_data['phone']:
            cleaned_data['phone'] = PHONE_REGEX.sub(r'\2\3\4', cleaned_data['phone'])

        return cleaned_data

    class Meta:
        model = Person
        fields = [
            'prefix', 'first_name', 'last_name', 'suffix',
            'bio', 'phone', 'email', 'website',
            'facebook', 'twitter', 'instagram',
        ]

class ContactForm(forms.ModelForm):
    prefix = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prefix (optional, e.g. Dr., Mr., Ms., etc.)',
            'autocomplete': 'off',
            'maxlength': 5,
        }),
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'autocomplete': 'off',
            'maxlength': 35,
        }),
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'autocomplete': 'off',
            'maxlength': 35,
        }),
    )
    suffix = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Suffix (optional, e.g. Jr., IV, M.D., etc.)',
            'autocomplete': 'off',
            'maxlength': 5,
        }),
    )
    image = forms.ImageField(
        required=False,
        label='Profile Image',
        widget=forms.FileInput(attrs={
            'class': 'col-12 col-md-8',
            'autocomplete': 'off',
        }),
    )
    clear_image = forms.BooleanField(
        required=False,
        label='Clear Existing Image',
    )
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title',
            'autocomplete': 'off',
            'maxlength': 70,
        }),
    )
    bio = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Bio',
            'autocomplete': 'off',
        }),
    )
    phone = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone (optional)',
            'autocomplete': 'off',
        }),
    )
    email = forms.EmailField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email (optional)',
            'autocomplete': 'off',
        }),
    )
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Website (optional)',
            'autocomplete': 'off',
        }),
    )
    facebook = forms.CharField(
        required=False,
        label='facebook.com/',
        widget=forms.TextInput(attrs={
            'class': 'col-12 col-md-6 form-control',
            'placeholder': '(optional)',
            'autocomplete': 'off',
        }),
    )
    twitter = forms.CharField(
        required=False,
        label='twitter.com/',
        widget=forms.TextInput(attrs={
            'class': 'col-12 col-md-6 form-control',
            'placeholder': '(optional)',
            'autocomplete': 'off',
        }),
    )
    instagram = forms.CharField(
        required=False,
        label='instagram.com/',
        widget=forms.TextInput(attrs={
            'class': 'col-12 col-md-6 form-control',
            'placeholder': '(optional)',
            'autocomplete': 'off',
        }),
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        if cleaned_data['phone']:
            cleaned_data['phone'] = PHONE_REGEX.sub(r'\2\3\4', cleaned_data['phone'])

        return cleaned_data

    class Meta:
        model = Contact
        fields = [
            'prefix', 'first_name', 'last_name', 'suffix',
            'bio', 'title', 'phone', 'email', 'website',
            'facebook', 'twitter', 'instagram',
        ]
