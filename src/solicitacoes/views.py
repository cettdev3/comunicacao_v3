from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Solicitacoes, Timeline, Demandas, Pecas,Entregas
from repositorio.models import Arquivos_Solicitacoes,Arquivos_Demandas
from perfil.models import Perfil
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .utils import *
from django.db import transaction
def timeline(solicitacao,autorId,descricao):
    lado_timeline = get_lado_timeline(solicitacao.id)
    timeline = Timeline.objects.create(
        autor_id = autorId,
        solicitacao_id = solicitacao.id,
        descricao = descricao,
        lado = lado_timeline

    )

def gera_demandas(solicitacao_id,designante,autor,prioridade):
    peca = Pecas.objects.create(solicitacao_id=solicitacao_id,titulo='Designar Demandas')
    demandas = Demandas.objects.create(designante_id=designante,autor_id=autor.id,prioridade=prioridade,peca_id=peca.id,status=1)
    return demandas

def convert_data_formatada(data):

    data = data.split('/')
    data = data[2]+'-'+data[1]+'-'+data[0]
    return data

@login_required(login_url='/')
def Solicitacao(request):

    # solicitacoes = Solicitacoes.objects.all().exclude(status=3).order_by('-id')
    solicitacoes = Solicitacoes.objects.all().order_by('-id')
    for solicitacao in solicitacoes:
        perfil = Perfil.objects.filter(user_profile_id=request.user.id).first()
        solicitacao.perfil = perfil
    solicitacoes_paginators = Paginator(solicitacoes,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)
    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = foto.cargo
    return render(request,'solicitacoes.html',{'paginas':page,'solicitacoes':solicitacoes,'foto':foto,'perm':perm})

@login_required(login_url='/')
def Paginar(request):
    solicitacoes = Solicitacoes.objects.all()
    solicitacoes_paginators = Paginator(solicitacoes,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)
    perfil = Perfil.objects.filter(user_profile_id=request.user.id).first()
    return render(request,'ajax/tbl_solicitacoes.html',{'paginas':page,'perfil':perfil})

@login_required(login_url='/')
def Filter_Solicitacoes(request):
    solicitacao_id = request.GET.get('idSolicitacao','')
    solicitacao = request.GET.get('solicitacao','')
    data_solicitacao = request.GET.get('data_solicitacao','')
    if data_solicitacao:
        data_solicitacao = convert_data_formatada(data_solicitacao)
    setor = request.GET.get('setor','')
    status = request.GET.get('status','')

    if solicitacao_id:
        sl = Solicitacoes.objects.filter(id=solicitacao_id)
    elif solicitacao:
        sl = Solicitacoes.objects.filter(id=solicitacao)
    elif data_solicitacao:
        sl = Solicitacoes.objects.filter(data_solicitacao=data_solicitacao)
    elif setor:
        sl = Solicitacoes.objects.filter(tipo_projeto=setor)
    elif status:
        sl = Solicitacoes.objects.filter(status=status)
    else:
        sl = Solicitacoes.objects.all()

    solicitacoes_paginators = Paginator(sl,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)
    perfil = Perfil.objects.filter(user_profile_id=request.user.id).first()
    return render(request,'ajax/tbl_solicitacoes.html',{'paginas':page,'perfil':perfil})

def Realizar_Solicitacao(request):
    with transaction.atomic():
        print(request.POST)
        arquivos = request.FILES.getlist('files[]')
        titulo = request.POST.get('titulo','')
        prazo_entrega = request.POST.get('prazo_entrega','')
        prazo_entrega = convert_data_formatada(prazo_entrega)
        destino = request.POST.get('destino','')
        briefing = request.POST.get('editordata','')
        prioridade = request.POST.get('prioridade','')
        
        
        if titulo:
            pass
        else:
            return JsonResponse({"error":True,"error_message": "Ops! Algo deu errado. Verifique se o título foi preenchido."}, status=400)
        
        if prazo_entrega:
            pass
        else:
            return JsonResponse({"error":True,"error_message": "Ops! Algo deu errado. Verifique se o prazo de entrega foi preenchido."}, status=400)
        
        if destino:
            pass
        else:
            return JsonResponse({"error":True,"error_message": "Ops! Algo deu errado. Verifique se o destino foi preenchido."}, status=400)


        if briefing:
            pass
        else:
            return JsonResponse({"error":True,"error_message": "Ops! Algo deu errado. Verifique se o briefing foi preenchido."}, status=400)
        
        solicitar = Solicitacoes.objects.create(
            titulo = titulo,
            prazo_entrega = prazo_entrega,
            tipo_projeto = destino,
            briefing = briefing,
            autor = request.user,
            status = 1

        )

        # lado = get_lado_timeline(solicitar.id)
        # timeline = Timeline.objects.create(
        #     autor = request.user,
        #     solicitacao_id = solicitar.id,
        #     descricao = f'{request.user.first_name} realizou a solicitação',
        #     lado = lado

        # )
        timeline(solicitar,request.user.id,f'{request.user.first_name} realizou a solicitação')
        solicitacoes = Solicitacoes.objects.all().exclude(status=3).order_by('-id')
        solicitacoes_paginators = Paginator(solicitacoes,50)
        page_num = request.GET.get('pagina')
        page = solicitacoes_paginators.get_page(page_num)

        perfil = Perfil.objects.filter(und=destino).first()

        gera_demanda = gera_demandas(solicitar.id,perfil.id,request.user,prioridade=prioridade)



        try:
            arquivos = request.FILES.getlist('files[]')
            for arquivo in arquivos:
                fs1 = FileSystemStorage()
                filename1 = fs1.save(arquivo.name, arquivo)
                arquivo_url = fs1.url(filename1)
                arquivos = Arquivos_Solicitacoes.objects.create(rota = arquivo_url,autor_id = request.user.id, solicitacao_id = solicitar.id)

        except:
            pass
        return render(request,'ajax/tbl_solicitacoes.html',{'paginas':page})

@login_required(login_url='/')
def LineTimeline(request,codigo):
    itens = Timeline.objects.filter(solicitacao_id=codigo).all().order_by('-id')
    for item in itens:
        perfil = Perfil.objects.filter(user_profile_id = item.autor_id).first()
        item.foto = perfil.foto

    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = foto.cargo
    
    return render(request,'timeline.html',{'itens':itens,'foto':foto,'perm':perm})	

@login_required(login_url='/')
def Entregas_Realizadas(request):
    
    solicitacao = request.GET.get('solicitacao_id','')
    entregas = Entregas.objects.filter(solicitacao_id=solicitacao).all().order_by('-id')
    for entrega in entregas:
        demanda_id = entrega.demanda_id
        arquivos_demandas = Arquivos_Demandas.objects.filter(demanda_id=demanda_id).all().order_by('-id')
        entrega.file_demandas = arquivos_demandas
        print(entrega.file_demandas)
    return render(request,'ajax/modal_show_entregas.html',{'entregas':entregas})

@login_required(login_url='/')
def Retifica_Solicitacao(request):
    solicitacao_id = request.GET.get('solicitacao_id','')
    solicitacao = Solicitacoes.objects.filter(id=solicitacao_id).first()
    arquivos_solicitacoes = Arquivos_Solicitacoes.objects.filter(solicitacao_id = solicitacao_id).all()
    solicitacao.arquivos_solicitacao = arquivos_solicitacoes
    return render(request,'ajax/modal_retifica_solicitacao.html',{'solicitacao':solicitacao})

@login_required(login_url='/')
def Retificar_Solicitacao(request):
    with transaction.atomic():
        id_solicitacao = request.POST.get('solicitacao_id','')
        titulo = request.POST.get('titulo','')
        prazo = request.POST.get('prazo','')
        destino = request.POST.get('destino','')
        briefing = request.POST.get('briefing','')
        prioridade = request.POST.get('prioridade','')
        
        solicitacao = Solicitacoes.objects.get(id=id_solicitacao)
        solicitacao.titulo = titulo
        solicitacao.prazo_entrega = prazo
        solicitacao.tipo_projeto = destino
        solicitacao.briefing = briefing
        solicitacao.prioridade = prioridade
        solicitacao.status = 1
        solicitacao.save() 


        #obter a peça da solicitação e redefinir para a fazer
        peca = Pecas.objects.filter(solicitacao_id=id_solicitacao,titulo='Designar Demandas').first()

        #obtem a demanda vinculada a peça acima
        demanda = Demandas.objects.get(peca_id=peca.id)
        demanda.status = 1
        demanda.save()
        return render(request,'ajax/modal_retifica_solicitacao.html',{'solicitacao':solicitacao})