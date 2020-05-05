from django import forms
from django.core.exceptions import PermissionDenied

from .models import Article
from images.models import Album

class CreateArticleForm(forms.ModelForm):
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
