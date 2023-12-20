from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Demandas, Solicitacoes,Pecas,Timeline
from django.core.files.storage import FileSystemStorage
from repositorio.models import Arquivos_Demandas
from django.http import JsonResponse
from django.db import transaction
from perfil.models import Perfil
from solicitacoes.utils import *
@login_required(login_url='/')
def Minhas_Tarefas(request):
    solicitacoes = Solicitacoes.objects.filter(pecas__demandas__designante=request.user).distinct()
    
    for solicitacao in solicitacoes:
        total_demandas = Demandas.objects.filter(peca__solicitacao=solicitacao).count()
        demandas_finalizadas = Demandas.objects.filter(peca__solicitacao=solicitacao, status=5).count()

        demandas_andamento = Demandas.objects.filter(peca__solicitacao=solicitacao, status=2).count()
        demandas_revisao = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=3).count()
        demandas_analise = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=4).count()
        solicitacao.total_demandas = total_demandas
        solicitacao.demandas_finalizadas = demandas_finalizadas
        solicitacao.demandas_andamento = demandas_andamento
        solicitacao.demandas_revisao = demandas_revisao
        solicitacao.demandas_analise = demandas_analise
        
    return render(request,'minhas_tarefas.html',{'solicitacoes':solicitacoes})

@login_required(login_url='/')
def Show_Modal_Task(request):
    req_solicitacao = request.GET.get('solicitacao_id','')
    solicitacao = Solicitacoes.objects.filter(id=req_solicitacao).first()
    
    pecas = Pecas.objects.filter(solicitacao=solicitacao, demandas__designante=request.user).distinct()
    for peca in pecas:
        demandas_relacionadas = Demandas.objects.filter(peca_id=peca.id).first()
        peca.demanda_relacionada = demandas_relacionadas
        arquivos_demandas = Arquivos_Demandas.objects.filter(demanda=demandas_relacionadas)
        peca.arquivos_relacionados = arquivos_demandas
        
    solicitacao.pecas = pecas

    return render(request,'ajax/ajax_task_detail.html',{'solicitacao':solicitacao})

@login_required(login_url='/')
def Concluir_Demanda(request):
    print(request.POST)
    print(request.FILES)

    with transaction.atomic():
        try:
            descricao = request.POST.get('editordata','')
            demandaId = request.POST.get('demandaId','')

            arquivos = request.FILES.getlist('files[]')
            for arquivo in arquivos:
                fs1 = FileSystemStorage()
                filename1 = fs1.save(arquivo.name, arquivo)
                arquivo_url = fs1.url(filename1)
                arquivos = Arquivos_Demandas.objects.create(rota = arquivo_url,autor_id = request.user.id, demanda_id = demandaId)
            
            

            und = Perfil.objects.filter(user_profile=request.user).first()
            demanda = Demandas.objects.get(id=demandaId)
            if und.und <= 4:
                demanda.status = 5
                description = f'{request.user.first_name} concluiu a designação'
            else:
                demanda.status = 4
                description = f'{request.user.first_name} concluiu a entrega e está em análise',
            demanda.descricao_entrega = descricao
            demanda.save()

            solicitacao_id = Demandas.objects.filter(id=demandaId).first().peca.solicitacao.id
            lado = get_lado_timeline(solicitacao_id)
            timeline = Timeline.objects.create(
                autor = request.user,
                solicitacao_id = solicitacao_id,
                descricao = description,
                lado = lado

    )

            return JsonResponse({"success":True,"success_message": "Entrega realizada com sucesso!"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error":True,"error_message": str(e)}, status=400)

@login_required(login_url='/')
def Cadastrar_Peca(request):
    