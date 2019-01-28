from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from perfis.models import Perfil 
from usuarios.forms import RegistrarUsuarioForm
from django.db import IntegrityError, transaction
from django.http import HttpResponse

# Create your views here.

class RegistarUsuarioView(View):

    template_name = 'registrar.html'

    def get(self,request):
        return render(request,self.template_name)
    
    @transaction.atomic
    def post(self,request):
        form = RegistrarUsuarioForm(request.POST) 
        if form.is_valid(): 
            dados_form = form.cleaned_data
            try:
                with transaction.atomic(): 
                    usuario = User.objects.create_user(username = dados_form['nome'], 
                                        email = dados_form['email'], 
                                        password = dados_form ['senha'])
            except:
                return render(request,"erro_transacao.html")
            perfil = Perfil(nome=dados_form['nome'], 
                            telefone=dados_form['telefone'], 
                            nome_empresa=dados_form['nome_empresa'],
                             usuario=usuario)
            try:
                with transaction.atomic():
                    #perfil.nome=None 
                    perfil.save()
            except IntegrityError:
                return render(request,"erro_transacao.html") 
            return redirect('index')
        return render(request, self.template_name, {'form' : form})
