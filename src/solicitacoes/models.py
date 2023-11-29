from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Solicitacoes(models.Model):
    choice_projeto = [('1','EFG'),('2','COTEC'),('3','CETT'),('4','BASILEU')]
    choices_status = [('1','EM ANÁLISE'),('2','EM PRODUÇÃO'),('3','CONCLUÍDA'),('4','DEVOLVIDA'),('5','CANCELADA')]

    id = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False,blank=False)
    motivo_devolucao = models.TextField(null=True,blank=True)
    tipo_projeto = models.IntegerField(choices=choice_projeto,null=False,blank=False)
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(default=timezone.now,null=False,blank=False)
    prazo_entrega = models.DateField(null=False,blank=False)
    briefing = models.TextField(null=False,blank=False)
    arquivos = models.TextField(null=True,blank=True)
    status = models.IntegerField(choices=choices_status,null=False,blank=False)

    def get_status_display(self):
        return dict(self.choices_status)[self.status]

    def get_projeto_display(self):
        return dict(self.choice_projeto)[self.tipo_projeto]

    class Meta:
        db_table = 'solicitacoes'