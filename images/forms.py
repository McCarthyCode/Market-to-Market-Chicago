from django import forms
from django.core.validators import MaxLengthValidator

from .models import Album, Image

class CreateAlbumForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title',
            'autocomplete': 'off',
        }),
        validators=[MaxLengthValidator(255)],
    )
    images = forms.ImageField(
        label='Images',
        widget=forms.FileInput(attrs={
            'class': 'col-12 col-md-8',
            'accept': 'image/*',
            'multiple': '',
        }),
    )
    feed = forms.BooleanField(
        required=False,
        label='View in News Feeds',
    )
    category = forms.ChoiceField(
        label='Category',
        choices=Album.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control col-12 col-md-6',
        }),
    )

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = Album
        fields = ['title', 'feed', 'category']

class UpdateAlbumTitleForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title',
        }),
    )

    class Meta:
        model = Album
        fields = ['title']

class AddImagesForm(forms.ModelForm):
    images = forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'multiple': '',
        }),
    )

    class Meta:
        model = Image
        fields = ['images']
