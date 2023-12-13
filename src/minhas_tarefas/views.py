from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Demandas, Solicitacoes,Pecas
@login_required(login_url='/')
def Minhas_Tarefas(request):
    solicitacoes = Solicitacoes.objects.filter(pecas__demandas__designante=request.user).distinct()
    
    for solicitacao in solicitacoes:
        total_demandas = Demandas.objects.filter(peca__solicitacao=solicitacao).count()
        demandas_finalizadas = Demandas.objects.filter(peca__solicitacao=solicitacao, status=4).count()

        demandas_andamento = Demandas.objects.filter(peca__solicitacao=solicitacao, status=2).count()
        demandas_revisao = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=3).count()
        solicitacao.total_demandas = total_demandas
        solicitacao.demandas_finalizadas = demandas_finalizadas
        solicitacao.demandas_andamento = demandas_andamento
        solicitacao.demandas_revisao = demandas_revisao
        
    return render(request,'minhas_tarefas.html',{'solicitacoes':solicitacoes})