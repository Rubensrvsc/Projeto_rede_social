from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=20, null= False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('Perfil')
    usuario = models.OneToOneField(User, related_name="perfil", on_delete = models.CASCADE,default="", editable=False) 

    def __str__(self):
        return self.nome

    @property 
    def email(self): 
        return self.usuario.email

    def convidar(self, perfil_convidado):
        #if self.pode_convidar(perfil_convidado):
        convite = Convite(solicitante=self,convidado = perfil_convidado)
        convite.save()

    def desfazer(self,perfil):
        self.contatos.remove(perfil)
        perfil.contatos.remove(self)

    def remove(self,perfil):
        pass


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):        
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()
    
    def recusar(self):
        self.delete()

'''class Timeline(models.Model):
    perfil = models.OneToOneField(Perfil,related_name='timeline',on_delete=models.CASCADE)'''

class Post(models.Model):
    texto = models.CharField(max_length=140)
    data = models.DateTimeField(auto_now=True)
    timeline = models.ForeignKey(Perfil, related_name = 'timeline' ,on_delete = models.CASCADE)