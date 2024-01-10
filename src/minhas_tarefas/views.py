from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Demandas, Solicitacoes,Pecas,Timeline
from django.core.files.storage import FileSystemStorage
from repositorio.models import Arquivos_Demandas
from django.http import JsonResponse
from django.db import transaction
from perfil.models import Perfil
from solicitacoes.utils import *
from django.contrib.auth.models import User
from django.db import transaction

@login_required(login_url='/')
def Minhas_Tarefas(request):
    solicitacoes = Solicitacoes.objects.filter(pecas__demandas__designante=request.user).distinct()
    
    for solicitacao in solicitacoes:
        total_demandas = Demandas.objects.filter(peca__solicitacao=solicitacao,designante_id = request.user.id).count()
        demandas_finalizadas = Demandas.objects.filter(peca__solicitacao=solicitacao, status=5, designante_id = request.user.id).count()

        demandas_andamento = Demandas.objects.filter(peca__solicitacao=solicitacao, status=2,designante_id = request.user.id).count()
        demandas_revisao = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=3,designante_id = request.user.id).count()
        demandas_analise = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=4,designante_id = request.user.id).count()
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
    usuarios = User.objects.all()
    pecas = Pecas.objects.filter(solicitacao=solicitacao, demandas__designante=request.user).distinct()
    all_pecas = Pecas.objects.filter(solicitacao_id = solicitacao.id).all()

    for peca in pecas:
        demandas_relacionadas = Demandas.objects.filter(peca_id=peca.id).first()
        peca.demanda_relacionada = demandas_relacionadas
        arquivos_demandas = Arquivos_Demandas.objects.filter(demanda=demandas_relacionadas)
        peca.arquivos_relacionados = arquivos_demandas
    
    for peca in all_pecas:
        demandas_relacionadas = Demandas.objects.filter(peca=peca)
        peca.demandas_relacionadas = demandas_relacionadas

    solicitacao.pecas = pecas
    solicitacao.todas_pecas = all_pecas
    solicitacao.usuarios = usuarios


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
    print(request.POST)
    solicitacaoId = request.POST.get('solicitacao_id','')
    peca = request.POST.get('peca','')

    peca = Pecas.objects.create(titulo=peca,solicitacao_id = solicitacaoId)
    todas_pecas = Pecas.objects.filter(solicitacao_id = solicitacaoId).all()
    return render(request,'ajax/ajax_tbl_pecas.html',{'pecas':todas_pecas})

@login_required(login_url='/')
def Designar_Usuário(request):
    with transaction.atomic():
        try:
            solicitacao = request.POST.get('solicitacao_id','')
            peca = request.POST.get('peca','')
            usuario = request.POST.get('usuario_id','')
            prioridade = request.POST.get('prioridade','')

            demanda = Demandas.objects.create(peca_id = peca,designante_id = usuario,autor_id = request.user.id,prioridade = prioridade,status = 1)

            all_pecas = Pecas.objects.filter(solicitacao_id = solicitacao).all()
            for peca in all_pecas:
                demandas_relacionadas = Demandas.objects.filter(peca=peca)
                peca.demandas_relacionadas = demandas_relacionadas

            print(all_pecas.values())

            return render(request,'ajax/ajax_tbl_designacao.html',{'pecas':all_pecas})
        except Exception as e:
            print(e)

@login_required(login_url='/')
def alterarSolicitacao(request):
    prazo_entrega = request.POST.get('prazo','')
    prioridade = request.POST.get('prioridade','')
    briefing = request.POST.get('briefing','')
    solicitacao_id = request.POST.get('solicitacao_id','')

    solicitacao = Solicitacoes.objects.get(id=solicitacao_id)
    solicitacao.prazo_entrega = prazo_entrega
    solicitacao.prioridade = prioridade
    solicitacao.briefing = briefing
    solicitacao.save()

    return JsonResponse({"success_message": "Solicitação Alterada!"}, status=200)

@login_required(login_url='/')
def devolveSolicitacao(request):
    solicitacao_id = request.POST.get('solicitacao_id','')
    motivo = request.POST.get('motivo','')

    solicitacao = Solicitacoes.objects.get(id=solicitacao_id)
    solicitacao.motivo_devolucao = motivo
    solicitacao.status = 4

    solicitacao.save()

    return JsonResponse({"success_message": "Solicitação Devolvida!"}, status=200)

@login_required(login_url='/')
def showDemandaModal(request):
    demanda_id = request.GET.get('demandaid','')
    demanda = Demandas.objects.filter(id=demanda_id).first()
    arquivos_demandas = Arquivos_Demandas.objects.filter(demanda_id=demanda_id).all()
    demanda.arquivos_demandas = arquivos_demandas


    return render(request,'ajax/ajax_demanda_task.html',{'demanda':demanda}) 