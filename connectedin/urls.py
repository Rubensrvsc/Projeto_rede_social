"""connectedin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from perfis import views 
from usuarios.views import RegistarUsuarioView
from django.contrib.auth import views as v
from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView,
PasswordResetConfirmView,PasswordResetCompleteView)
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('perfil/<int:perfil_id>', views.exibir_perfil, name='exibir'),
    path('perfil/<int:perfil_id>/convidar',views.convidar, name='convidar'),
    path('convite/<int:convite_id>/aceitar',views.aceitar, name='aceitar'),
    path('convite/<int:convite_id>/recusar',views.recusar, name='recusar'),
    path('convite/<int:perfil_id>/desfazer',views.desfazer_amizade, name='desfazer'),
    path('registrar/',RegistarUsuarioView.as_view(),name='registrar'),
    path('perfil/alterar_senha',views.alterar_senha,name='alterar_senha'),
    path('login/', v.LoginView.as_view(template_name='login.html'), name = 'login'), 
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name="logout"),
    path('perfil/pesquisar',views.pesquisar,name='pesquisar'),
    path('perfil/mostrar',views.realizar_pesquisa,name='realizar_pesquisa'),
    path('perfil/timeline',views.exibir_timeline,name='timeline'),
    path('perfil/post',views.incluir_post,name='incluir_post'),
    path('perfil/<int:id_post>/excluir',views.excluir_post,name='excluir_post'),
    path('', include('django.contrib.auth.urls')),
    path('perfil/<int:perfil_id>/super_user',views.is_super_user,name='superuser'),
    path('<int:perfil_id>/bloquear', views.bloquear_usuario, name='bloquear'),
    path('<int:perfil_id>/desbloquear', views.desbloquear_usuario, name='desbloquear'),
<<<<<<< HEAD
=======
    path('perfil/desativar',views.desativa_perfil,name='desativar_perfil'),
    path('perfil/reativar',views.reativar_perfil,name='reativar_perfil'),
<<<<<<< HEAD
>>>>>>> 31aed2b4c36322ea5a19b48ce3fb42eb90e6cf7c
=======
    path('perfil/adicionar_foto',views.adicionar_foto,name='adicionar_foto'),
>>>>>>> novas_questoes

     url(r'^reset-password/$', PasswordResetView.as_view( template_name='reset_password.html',
    success_url=reverse_lazy('password_reset_done'),email_template_name ='reset_password_email.html'), name='reset_password'),

    url(r'^reset-password/done/$', PasswordResetDoneView.as_view(template_name= 'reset_password_done.html'), name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view( template_name='reset_password_confirm.html',
    success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),

    url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(template_name= 'reset_password_complete.html'), name='password_reset_complete')

]
if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
