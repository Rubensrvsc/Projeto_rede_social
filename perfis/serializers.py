from rest_framework import serializers
from .models import *

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model=Perfil
        fields=('id','nome','nome_empresa','is_ativo',)

class PostSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('id','texto','photo_post','timeline',)