from django.db import models
from django.contrib.auth.models import User
from solicitacoes.models import Solicitacoes, Demandas
# Create your models here.
class Arquivos_Solicitacoes(models.Model):

    id = models.AutoField(primary_key=True)
    rota = models.TextField(null=True, blank=True)
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    solicitacao = models.ForeignKey(Solicitacoes,on_delete=models.CASCADE)

    class Meta:
        db_table = 'arquivos_solicitacoes'

class Arquivos_Demandas(models.Model):

    id = models.AutoField(primary_key=True)
    rota = models.TextField(null=True, blank=True)
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    demanda = models.ForeignKey(Demandas,on_delete=models.CASCADE)
    class Meta:
        db_table = 'arquivos_demandas'