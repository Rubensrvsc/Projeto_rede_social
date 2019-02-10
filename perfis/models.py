from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=20, null= False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('Perfil')
    photo = models.ImageField(upload_to='', null=True, blank = True)
    bloq = models.ManyToManyField('Perfil',related_name='bloqueado',null=True, blank=True)
    usuario = models.OneToOneField(User, related_name="perfil", on_delete = models.CASCADE,default="", editable=False)
    is_ativo = models.BooleanField(default=True)
    dinheiro=models.FloatField(default=0)

    def __str__(self):
        return self.nome

    @property 
    def email(self): 
        return self.usuario.email

    def depositar_dinheiro(self,qtd_dinheiro):
        self.dinheiro+=int(qtd_dinheiro)
        self.save()

    def desativar(self):
        self.is_ativo=False
        self.save()

    def reativar(self):
        self.is_ativo=True
        self.save()

    def convidar(self, perfil_convidado):
        #if self.pode_convidar(perfil_convidado):
        convite = Convite(solicitante=self,convidado = perfil_convidado)
        convite.save()
    
    def super_user(self):
        self.usuario.is_superuser=True
        self.usuario.save()


    def desfazer(self,perfil):
        self.contatos.remove(perfil)
        perfil.contatos.remove(self)

    def bloquear(self,perfil):
        if perfil==self:
            return
        else:
            self.bloq.add(perfil)
            self.desfazer(perfil)
            self.save()
    
    def desbloquear(self,perfil):
        if perfil==self:
            return
        else:
            self.bloq.remove(perfil)
            self.save()

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
    photo_post = models.ImageField(upload_to='',null=True, blank = True)
    timeline = models.ForeignKey(Perfil, related_name = 'timeline' ,on_delete = models.CASCADE)

class Status(models.Model):
    perfil = models.OneToOneField(Perfil,on_delete=models.CASCADE)
    justificativa = models.CharField(max_length=256)

#Anuciar vender produto
class Produto(models.Model):
    nome_produto=models.CharField(max_length=256)
    preco=models.FloatField()
    produto=models.ForeignKey(Perfil,related_name='produto',on_delete=models.CASCADE)
    
    def compra(self,perfil,qtd_dinheiro):
        perfil.produto.dinheiro-=qtd_dinheiro
        self.produto.dinheiro+=qtd_dinheiro
        perfil.produto.add(self).save()
        self.delete().save()
    
    def desconto(self,qtd_dinheiro):
        self.produto.dinheiro-=qtd_dinheiro
        self.produto.save()
    
    def salvar_produto(self,perfil):
        self.produto=perfil
        self.save()