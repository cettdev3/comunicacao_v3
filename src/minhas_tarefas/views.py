from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Demandas, Solicitacoes,Pecas,Timeline,Entregas
from repositorio.models import *
from django.core.files.storage import FileSystemStorage
from repositorio.models import Arquivos_Demandas
from django.http import JsonResponse
from django.db import transaction
from perfil.models import Perfil
from solicitacoes.utils import *
from django.contrib.auth.models import User
from django.db import transaction

def gera_demandas(solicitacao_id,designante,autor,prioridade,titulo,peca):
    # peca = Pecas.objects.create(solicitacao_id=solicitacao_id,titulo=titulo)
    demandas_recebidas = Demandas.objects.filter(designante_id = designante,peca_id=peca).first()
    if demandas_recebidas:
        demandas_recebidas.status = 1
        demandas_recebidas.save()
        demandas = demandas_recebidas
    else:
        demandas = Demandas.objects.create(designante_id=designante,autor_id=autor,prioridade=prioridade,peca_id=peca,status=1)
    return demandas

def timeline(solicitacao,autorId,descricao):
    lado_timeline = get_lado_timeline(solicitacao.id)
    timeline = Timeline.objects.create(
        autor_id = autorId,
        solicitacao_id = solicitacao.id,
        descricao = descricao,
        lado = lado_timeline

    )

@login_required(login_url='/')
def Minhas_Tarefas(request):
    solicitacoes = Solicitacoes.objects.filter(pecas__demandas__designante=request.user).distinct()
    
    for solicitacao in solicitacoes:
        total_demandas = Demandas.objects.filter(peca__solicitacao=solicitacao,designante_id = request.user.id).count()
        demandas_finalizadas = Demandas.objects.filter(peca__solicitacao=solicitacao, status=5, designante_id = request.user.id).count()

        demandas_andamento = Demandas.objects.filter(peca__solicitacao=solicitacao, status=2,designante_id = request.user.id).count()
        demandas_revisao = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=3,designante_id = request.user.id).count()
        demandas_analise = Demandas.objects.filter(peca__solicitacao=solicitacao).filter(status=4,designante_id = request.user.id).count()
        demandas_entregues = Demandas.objects.filter(peca__solicitacao=solicitacao, status=6,designante_id = request.user.id).count()
        solicitacao.total_demandas = total_demandas
        solicitacao.demandas_finalizadas = demandas_finalizadas + demandas_entregues
        solicitacao.demandas_andamento = demandas_andamento
        solicitacao.demandas_revisao = demandas_revisao
        solicitacao.demandas_analise = demandas_analise
        solicitacao.demandas_entregues = demandas_entregues
        
    return render(request,'minhas_tarefas.html',{'solicitacoes':solicitacoes})

@login_required(login_url='/')
def Show_Modal_Task(request):
    req_solicitacao = request.GET.get('solicitacao_id','')
    solicitacao = Solicitacoes.objects.filter(id=req_solicitacao).first()
    arquivos_solicitacao = Arquivos_Solicitacoes.objects.filter(solicitacao_id = solicitacao.id).all()
    usuarios = User.objects.all()
    pecas = Pecas.objects.filter(solicitacao=solicitacao, demandas__designante_id=request.user.id).distinct()

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
    solicitacao.arquivos = arquivos_solicitacao


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
                description = f'{request.user.first_name} concluiu a entrega e está em análise'
            demanda.descricao_entrega = descricao
            demanda.save()

            solicitacao_id = Demandas.objects.filter(id=demandaId).first().peca.solicitacao.id
            solicitacao = Solicitacoes.objects.get(id=solicitacao_id)
            timeline(solicitacao,request.user.id,description)
            if und.und == 5:
                gera_demandas(solicitacao_id,demanda.autor_id,request.user.id,1,f'{demanda.peca.titulo} de {request.user.first_name}',demanda.peca_id)

            return JsonResponse({"success":True,"success_message": "Entrega realizada com sucesso!"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error":True,"error_message": str(e)}, status=400)

@login_required(login_url='/')
def Cadastrar_Peca(request):
    print(request.POST)
    solicitacaoId = request.POST.get('solicitacao_id','')
    solicitacao = Solicitacoes.objects.get(id=solicitacaoId)
    peca_name = request.POST.get('peca','')

    peca = Pecas.objects.create(titulo=peca_name,solicitacao_id = solicitacaoId)
    todas_pecas = Pecas.objects.filter(solicitacao_id = solicitacaoId).all()

    timeline(solicitacao,request.user.id,f'{request.user.first_name} cadastrou a peça {peca_name}')
    return render(request,'ajax/ajax_tbl_pecas.html',{'pecas':todas_pecas})

@login_required(login_url='/')
def Designar_Usuário(request):
    with transaction.atomic():
        peca = request.POST.get('peca','')
        is_demanda = Demandas.objects.filter(peca_id=peca,designante_id = request.POST.get('usuario_id','')).first()
        if is_demanda:
            return JsonResponse({"error":True,"error_message": "Não é possível realizar duas designações para uma mesma peça de um mesmo usuário!"}, status=400)
        else:
            try:
                solicitacao = request.POST.get('solicitacao_id','')
                solicitacao_ = Solicitacoes.objects.get(id=solicitacao)

                
                peca_ = Pecas.objects.filter(id=peca).first()
                usuario = request.POST.get('usuario_id','')
                prioridade = request.POST.get('prioridade','')
                profile = User.objects.filter(id=usuario).first()

                demanda = Demandas.objects.create(peca_id = peca,designante_id = usuario,autor_id = request.user.id,prioridade = prioridade,status = 1)

                all_pecas = Pecas.objects.filter(solicitacao_id = solicitacao).all()
                for peca in all_pecas:
                    demandas_relacionadas = Demandas.objects.filter(peca=peca)
                    peca.demandas_relacionadas = demandas_relacionadas

                timeline(solicitacao_,request.user.id,f'{request.user.first_name} designou {profile.first_name} a realizar uma atividade em {peca_.titulo}.')

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
    perfil = Perfil.objects.filter(user_profile_id = request.user.id).first()
    demanda_id = request.GET.get('demandaid','')
    demanda = Demandas.objects.filter(id=demanda_id).first()
    arquivos_demandas = Arquivos_Demandas.objects.filter(demanda_id=demanda_id).all()
    demanda.arquivos_demandas = arquivos_demandas


    return render(request,'ajax/ajax_demanda_task.html',{'demanda':demanda,'perfil':perfil}) 

@login_required(login_url='/')
def revisaDemanda(request):
    demanda_id = request.POST.get('demandaID','')
    motivo = request.POST.get('motivo','')
    status = request.POST.get('status','')
    solicitacao = Demandas.objects.filter(id=demanda_id).first().peca.solicitacao


    if status == '3':
        demanda = Demandas.objects.get(id=demanda_id)
        demanda.status = 3
        demanda.devolutiva = motivo
        demanda.save()
        timeline(solicitacao,request.user.id,f'{request.user.first_name} revisou a demanda de {demanda.designante.first_name} na peça {demanda.peca.titulo}.')

    elif status == '5':
        demanda = Demandas.objects.get(id=demanda_id)
        demanda.status = 5
        demanda.save()
        if request.user.id == demanda.designante_id:
            timeline(solicitacao,request.user.id,f'{request.user.first_name} finalizou a designação da demanda na peça {demanda.peca.titulo}.')
        else:
            timeline(solicitacao,request.user.id,f'{request.user.first_name} aprovou a entrega da demanda de {demanda.designante.first_name} na peça {demanda.peca.titulo}.')
    
    elif status == '6':
        demanda = Demandas.objects.get(id=demanda_id)
        entregas_realizadas = Entregas.objects.filter(demanda_id=demanda_id).count()
        if entregas_realizadas == 0:
            entrega = Entregas.objects.create(demanda_id=demanda_id,solicitacao_id=solicitacao.id)



        demanda.status = 6
        demanda.save()

    elif status == '1':
        demanda = Demandas.objects.get(id=demanda_id)
        demanda.status = 1
        demanda.save()
        timeline(solicitacao,request.user.id,f'{request.user.first_name} reabriu a demanda de {demanda.designante.first_name} na peça {demanda.peca.titulo}.')

    return JsonResponse({"success_message": "Solicitação Devolvida!"}, status=200)