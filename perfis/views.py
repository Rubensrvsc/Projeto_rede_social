from perfis.models import Perfil, Convite,Post
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponseNotFound,HttpResponseRedirect,HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from .serializers import *
from rest_framework.response import Response

@login_required
def index(request):
    usuarioLogado = request.user.perfil
    if request.user.is_superuser is True:
        perfil=Perfil.objects.all()
        paginator = Paginator(perfil,5)
        page = request.GET.get('page')
        perfis=paginator.get_page(page)
        return render(request,'pagina_super_user.html',{'perfis':perfis
        ,'usuarioLogado': usuarioLogado})
    else:
        post = [post for post in request.user.perfil.timeline.all()]
        contatos = request.user.perfil.contatos.all()
        for contato in contatos:
            for p in contato.timeline.all():
                post.append(p)
        paginator = Paginator(post,2)
        page = request.GET.get('page')
        posts=paginator.get_page(page)

        perfil=Perfil.objects.all()
        paginator = Paginator(perfil,5)
        page = request.GET.get('page')
        perfis=paginator.get_page(page)
        return render(request, 'index.html',{'perfis' : perfis,
        'posts':posts, 'usuarioLogado': usuarioLogado})

@api_view(['GET'])
#@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@login_required
def exibir_perfil(request, perfil_id):

    if request.method=='GET':
        perfil = Perfil.objects.get(id=perfil_id)
        if not request.user.perfil in perfil.bloq.all():
            perfil_serializer=PerfilSerializer(perfil)
            return render(request, 'perfil.html',{'perfil' : perfil_serializer.data, 'perfil_logado' : get_perfil_logado(request)})
        else:
            return redirect('index')


@api_view(['GET'])
def ver_perfil(request, perfil_id):

    if request.method=='GET':
        perfil = Perfil.objects.get(id=perfil_id)
        perfil_serializer=PerfilSerializer(perfil)
        return Response(perfil_serializer.data)


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
def adicionar_foto(request):
    perfil = request.user.perfil
    perfil.photo = request.GET['photo']
    perfil.save()
    return redirect('index')

@login_required
def realizar_pesquisa(request):
	nome=request.GET['nome']
	perfis = Perfil.objects.filter(nome__contains=nome)
	return render(request,'mostrar_pesquisa.html',{'perfil':perfis})

@transaction.atomic
@login_required
def exibir_timeline(request):
    if request.user.is_superuser is True:
        post = [post for post in request.user.perfil.timeline.all()]
        usuarioLogado = request.user.perfil
        contatos = request.user.perfil.contatos.all()
        for contato in contatos:
            for p in contato.timeline.all():
                post.append(p)
        paginator = Paginator(post,2)
        page = request.GET.get('page')
        posts=paginator.get_page(page)
        return render(request, 'timeline.html', {'posts': posts, 'usuarioLogado': usuarioLogado})
    else:
        return render(request,'erro.html')

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
@login_required
def incluir_post(request):
    if request.method == 'POST':
        postform = PostForm(request.POST,request.FILES or None)
        if postform.is_valid() :
            postinstance = postform.save(commit=False)
            postinstance.timeline=request.user.perfil
            postinstance.save()
            return redirect('index')
    else:
        postform=PostForm()
    return render(request,'add_post.html',{'post':postform})

@api_view(['GET','DELETE'])
@permission_classes((IsAuthenticated,))
@login_required
def excluir_post(request,id_post):
    if request.method is not 'POST':
        post_delete=Post.objects.filter(id=id_post)
        post_delete.delete()
        return redirect('index')

@login_required
def is_super_user(request,perfil_id):
    if request.user.is_superuser==True:
    	perfil=Perfil.objects.get(id=perfil_id)
    	perfil.super_user()
    	return redirect('index')
    else:
    	return render(request,'erro.html')

@login_required
def bloquear_usuario(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    request.user.perfil.bloquear(perfil)
    

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

@login_required
def password_reset_confirm(request,uidb,token):
    send_mail('Subject here', 'mensagem', settings.EMAIL_HOST_USER,
          [request.user.email], fail_silently=False)

@login_required
def desativa_perfil(request):
    form = JustificativaForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            request.user.perfil.desativar()
            instance = form.save(commit=False)
            instance.perfil = request.user.perfil
            instance.perfil.save()
            return redirect('index')
    else:
        form = JustificativaForm()
    return render(request,'justificativa.html',{'form':form})

@login_required
def reativar_perfil(request):
    request.user.perfil.reativar()
    return redirect('index')

@login_required
def criar_token(request):
    Token.objects.get_or_create(user=request.user)
    return redirect('index')

