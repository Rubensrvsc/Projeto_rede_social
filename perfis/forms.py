from django import forms
from django.forms import ModelForm
from .models import *

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=('texto',)

class PhotoPerfil(ModelForm):
    class Meta:
        model = Perfil
        fields = ['photo']