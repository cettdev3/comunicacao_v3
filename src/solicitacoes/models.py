from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from perfil.models import Perfil
# Create your models here.
class Solicitacoes(models.Model):
    choice_projeto = [(1,'EFG'),(2,'COTEC'),(3,'CETT'),(4,'BASILEU')]
    choices_status = [(1,'EM ANÁLISE'),(2,'EM PRODUÇÃO'),(3,'CONCLUÍDA'),(4,'DEVOLVIDA'),(5,'CANCELADA')]

    id = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False,blank=False)
    motivo_devolucao = models.TextField(null=True,blank=True)
    tipo_projeto = models.IntegerField(choices=choice_projeto,null=False,blank=False)
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(default=timezone.now,null=False,blank=False)
    prazo_entrega = models.DateField(null=False,blank=False)
    briefing = models.TextField(null=False,blank=False)
    status = models.IntegerField(choices=choices_status,null=False,blank=False)

    def get_status_display(self):
        return dict(self.choices_status)[self.status]

    def get_projeto_display(self):
        return dict(self.choice_projeto)[self.tipo_projeto]

    class Meta:
        db_table = 'solicitacoes'


class Pecas(models.Model):
   
    id = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False,blank=False)
    solicitacao = models.ForeignKey(Solicitacoes,on_delete=models.CASCADE)

    class Meta:
        db_table = 'pecas'


class Demandas(models.Model):
    choice_status = [(1,'A Fazer'),(2,'Em Progresso'),(3,'Em Revisão'),(4,'Concluído')]
    id = models.AutoField(primary_key=True)
    peca = models.ForeignKey(Pecas,on_delete=models.CASCADE)
    designante = models.ForeignKey(User,on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name='designante',on_delete=models.CASCADE)
    data_designacao = models.DateField(default=timezone.now, null=True, blank=True)
    status = models.IntegerField(choices=choice_status,null=False,blank=False)

    class Meta:
        db_table = 'demandas'


class Timeline(models.Model):
    id = models.AutoField(primary_key=True)
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateTimeField(default=timezone.now, null=True, blank=True)
    solicitacao = models.ForeignKey(Solicitacoes,on_delete=models.CASCADE)
    lado = models.IntegerField(null=True, blank=True)

    @property
    def cargo(self):
        meu_cargo = Perfil.objects.filter(user_profile=self.autor).first()
        return meu_cargo.get_cargo_display()
    
    class Meta:
        db_table = 'timeline'