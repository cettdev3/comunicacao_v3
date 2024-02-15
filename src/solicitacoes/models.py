from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from perfil.models import Perfil
# Create your models here.

def demandas_update(self):
    pecas = Pecas.objects.filter(solicitacao=self)
    demandas = Demandas.objects.filter(peca__in=pecas).count()
    demandas_concluidas = Demandas.objects.filter(peca__in=pecas).filter(status=5).count()
    demandas_enviadas = Demandas.objects.filter(peca__in=pecas).filter(status=6).count()
    print(pecas.count())

    if demandas_concluidas == demandas and pecas.count() > 1:
        self.status = 3
        self.save()
    elif demandas_concluidas > 0 and demandas_concluidas < demandas and demandas_enviadas == 0 and pecas.count() > 1:
        self.status = 2
        self.save()
    elif demandas_enviadas >= 1 and pecas.count() > 1:
        self.status = 6
        self.save()
    
    elif self.status == 4:
        return demandas
    
    else:
        self.status = 1
        self.save()

    return demandas

class Solicitacoes(models.Model):
    choice_projeto = [(1,'EFG'),(2,'COTEC'),(3,'CETT'),(4,'BASILEU')]
    choices_status = [(1,'EM ANÁLISE'),(2,'EM PRODUÇÃO'),(3,'AGUARDANDO ENTREGAS'),(4,'DEVOLVIDA'),(5,'CANCELADA'),(6,'ENTREGAS REALIZADAS')]
    choice_prioridade = [(1,'Normal'),(2,'Urgente')]
    id = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False,blank=False)
    motivo_devolucao = models.TextField(null=True,blank=True)
    tipo_projeto = models.IntegerField(choices=choice_projeto,null=False,blank=False)
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(default=timezone.now,null=False,blank=False)
    prazo_entrega = models.DateField(null=False,blank=False)
    briefing = models.TextField(null=False,blank=False)
    prioridade = models.IntegerField(choices=choice_prioridade,null=False,blank=False,default=1)
    status = models.IntegerField(choices=choices_status,null=False,blank=False)

    @property
    def count_demandas(self):
        pecas = Pecas.objects.filter(solicitacao=self)
        demandas = Demandas.objects.filter(peca__in=pecas).count()
        
        return demandas
    
    
    def get_prioridade_display(self):
        return dict(self.choice_prioridade)[self.prioridade]
    
    def get_status_display(self):
        demandas_update(self)
        return dict(self.choices_status)[self.status]

    def get_projeto_display(self):
        return dict(self.choice_projeto)[self.tipo_projeto]

    def is_prazo_vencido(self):
        return self.prazo_entrega < timezone.now().date()
    
    class Meta:
        db_table = 'solicitacoes'


class Pecas(models.Model):
   
    id = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False,blank=False)
    solicitacao = models.ForeignKey(Solicitacoes,on_delete=models.CASCADE)

    class Meta:
        db_table = 'pecas'


class Demandas(models.Model):
    choice_status = [(1,'A Fazer'),(2,'Em Progresso'),(3,'Em Revisão'),(4,'Em Análise'),(5,'Concluído'),(6,'Entregue')]
    choice_prioridade = [(1,'Normal'),(2,'Urgente')]
    id = models.AutoField(primary_key=True)
    peca = models.ForeignKey(Pecas,on_delete=models.CASCADE,null=False,blank=False)
    designante = models.ForeignKey(User,on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name='designante',on_delete=models.CASCADE)
    data_designacao = models.DateField(default=timezone.now, null=True, blank=True) 
    prioridade = models.IntegerField(choices=choice_prioridade,null=False,blank=False,default=1)
    descricao_entrega = models.TextField(null=False,blank=False,default="Nenhuma Descrição de Entrega")
    devolutiva = models.TextField(null=False,blank=False,default="")
    status = models.IntegerField(choices=choice_status,null=False,blank=False)

    def get_status_display(self):
        return dict(self.choice_status)[self.status]
    
    def get_prioridade_display(self):
        return dict(self.choice_prioridade)[self.prioridade]
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

class Entregas(models.Model):
    id = models.AutoField(primary_key=True)
    demanda = models.ForeignKey(Demandas,on_delete=models.CASCADE)
    solicitacao = models.ForeignKey(Solicitacoes,on_delete=models.CASCADE)

    class Meta:
        db_table = 'entregas'