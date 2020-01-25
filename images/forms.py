from django import forms
from .models import Album, Image

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
    image = forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={
            'accept': 'image/x-png,image/gif,image/jpeg',
            'multiple': '',
        }),
    )

    class Meta:
        model = Image
        fields = ['image']
