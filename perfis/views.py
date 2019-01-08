from perfis.models import Perfil, Convite,Post
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponseNotFound,HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.urls import reverse

@login_required
def index(request):
	return render(request, 'index.html',{'perfis' : Perfil.objects.all(),'perfil_logado' : get_perfil_logado(request)})

@login_required
def exibir_perfil(request, perfil_id):

        perfil = Perfil.objects.get(id=perfil_id)
        if not request.user.perfil in perfil.bloq.all():
            return render(request, 'perfil.html',{'perfil' : perfil, 'perfil_logado' : get_perfil_logado(request)})
        else:
            return redirect('index')

@login_required
def convidar(request,perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	
	#if(perfil_logado.pode_convidar(perfil_a_convidar)):
	perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('index')

@login_required
def get_perfil_logado(request):
	#if request.user.is_authenticated:
	profile=request.user.perfil
	return profile
	#else: 
		#return HttpResponseNotFound('sem perfil')

@login_required
def recusar(request,convite_id):
    convite=Convite.objects.get(id=convite_id)
    convite.recusar()
    return redirect('index')

@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('index')

@login_required
def desfazer_amizade(request,perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)
	perfil.desfazer(get_perfil_logado(request))
	return redirect('index')

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('index'))
        else:
            return redirect(reverse('alterar_senha'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'alterar_senha.html', args)

@login_required
def pesquisar(request):
    return render(request,'pesquisa_usuario.html')

@login_required
def realizar_pesquisa(request):
	nome=request.GET['nome']
	perfis = Perfil.objects.filter(nome__contains=nome)
	return render(request,'mostrar_pesquisa.html',{'perfil':perfis})
	pass

@login_required
def exibir_timeline(request):
    posts = [post for post in request.user.perfil.timeline.all()]
    usuarioLogado = request.user.perfil
    print(posts)
    contatos = request.user.perfil.contatos.all()
    for contato in contatos:
        for post in contato.timeline.all():
            posts.append(post)

    return render(request, 'timeline.html', {'posts': posts, 'usuarioLogado': usuarioLogado})


@login_required
def incluir_post(request):
    if request.method == 'POST':
        postform = PostForm(request.POST or None)
        if postform.is_valid():
            postinstance = postform.save(commit=False)
            postinstance.timeline=request.user.perfil
            postinstance.save()
            return redirect('index')
    else:
        postform=PostForm()
    return render(request,'add_post.html',{'post':postform})

@login_required
def excluir_post(request,id_post):
    Post.objects.filter(id=id_post).delete()
    return redirect('timeline')

@login_required
def is_super_user(request,perfil_id):
    if request.user.is_superuser==True:
    	perfil=Perfil.objects.get(id=perfil_id)
    	perfil.super_user()
    	perfil.save()
    	return redirect('index')
    else:
    	return render(request,'erro.html')
    
@login_required
def bloquear_usuario(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    request.user.perfil.bloquear(perfil)
    return redirect('index')

@login_required
def desbloquear_usuario(request,perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    request.user.perfil.desbloquear(perfil)
    return redirect('index')
