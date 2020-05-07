from django import forms
from django.core.exceptions import PermissionDenied

from .models import Author, Article
from images.models import Album
from mtm.settings import PHONE_REGEX

class AuthorForm(forms.ModelForm):
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
        widget=forms.ClearableFileInput(attrs={
            'class': 'col-12 col-md-8',
            'autocomplete': 'off',
        }),
    )
    bio = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Bio (optional)',
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

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        if cleaned_data['phone']:
            cleaned_data['phone'] = PHONE_REGEX.sub(r'\2\3\4', cleaned_data['phone'])

        return cleaned_data

    class Meta:
        model = Author
        fields = [
            'prefix', 'first_name', 'last_name', 'suffix',
            'image', 'bio', 'phone', 'email', 'website',
        ]

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title',
        }),
    )
    author = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Author',
        }),
    )
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Body',
        }),
    )
    album = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Photo Album (search for existing or leave blank)',
            'autocomplete': 'off',
        }),
    )
    album_id = forms.CharField(
        required=False,
        label='',
        widget=forms.HiddenInput(attrs={
            'autocomplete': 'off',
        }),
    )
    category = forms.ChoiceField(
        label='Category',
        choices=Article.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control col-12 col-md-6',
        }),
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        if 'album_id' not in cleaned_data:
            cleaned_data['album'] = None
        elif cleaned_data['album_id'] == '':
            cleaned_data['album'] = None

            del cleaned_data['album_id']
        else:
            album_id = int(cleaned_data['album_id'])
            if album_id == 0:
                cleaned_data['album'] = None
            else:
                try:
                    album = Album.objects.get(id=album_id)
                except Album.DoesNotExist:
                    raise forms.ValidationError('The specified album could not be found.')

                cleaned_data['album'] = album

            del cleaned_data['album_id']

        return cleaned_data

    class Meta:
        model = Article
        fields = ['title', 'author', 'body', 'album', 'category']
