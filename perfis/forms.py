from django import forms
from django.forms import ModelForm
from .models import *

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=('texto','photo_post',)

class JustificativaForm(ModelForm):
    class Meta:
        model = Status
        fields = ('justificativa',)

class PhotoPerfil(ModelForm):
    class Meta:
        model = Perfil
        fields = ['photo']

class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ('nome_produto','preco',)