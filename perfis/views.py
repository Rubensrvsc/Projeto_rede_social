from perfis.models import Perfil, Convite,Post
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponseNotFound,HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login, logout

@login_required
def index(request):
	return render(request, 'index.html',{'perfis' : Perfil.objects.all(),'perfil_logado' : get_perfil_logado(request)})

@login_required
def exibir_perfil(request, perfil_id):

	perfil = Perfil.objects.get(id=perfil_id)

	return render(request, 'perfil.html',
		          {'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request)})

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
	return render(request,'alterar_senha.html')
	'''buscar a senha do usuario, mostrar e mandar ele
	digitar uma nova senha para ser salva'''
@login_required
def mudar_senha(request):
	senha=request.GET['nova_senha']
	perfil=request.user
	perfil.set_password(senha)
	#perfil.usuario.password=senha
	perfil.save()
	perfil_autenticado=authenticate(username=request.user.username,password=senha)
	login(request,perfil_autenticado)
	return redirect('index')

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
    posts=request.user.perfil.timeline
    return render(request,'timeline.html',{'posts':posts})

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
    
def recuperar_senha(request):
    '''O usuario fornece o email e nome e o sistema busca no banco o seu registro
	para mudança de senha'''
