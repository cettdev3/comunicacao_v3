from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Solicitacoes, Timeline
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .utils import *

def convert_data_formatada(data):

    data = data.split('/')
    data = data[2]+'-'+data[1]+'-'+data[0]
    return data

@login_required(login_url='/')
def Solicitacao(request):
    solicitacoes = Solicitacoes.objects.all().exclude(status=3).order_by('-id')
    solicitacoes_paginators = Paginator(solicitacoes,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)
    return render(request,'solicitacoes.html',{'paginas':page,'solicitacoes':solicitacoes})

@login_required(login_url='/')
def Paginar(request):
    solicitacoes = Solicitacoes.objects.all()
    solicitacoes_paginators = Paginator(solicitacoes,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)

    return render(request,'ajax/tbl_solicitacoes.html',{'paginas':page})

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
    return render(request,'ajax/tbl_solicitacoes.html',{'paginas':page})

def Realizar_Solicitacao(request):
    print(request.POST)
    arquivos = request.FILES.getlist('files[]')
    titulo = request.POST.get('titulo','')
    prazo_entrega = request.POST.get('prazo_entrega','')
    prazo_entrega = convert_data_formatada(prazo_entrega)
    destino = request.POST.get('destino','')
    briefing = request.POST.get('editordata','')
    try:
        arquivos_solicitacao = []
        arquivos = request.FILES.getlist('files[]')
        for arquivo in arquivos:
            fs1 = FileSystemStorage()
            filename1 = fs1.save(arquivo.name, arquivo)
            arquivo_url = fs1.url(filename1)
            arquivos_solicitacao.append(arquivo_url)
    except:
        arquivo_url = []
    
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

    lado = get_lado_timeline(solicitar.id)
    timeline = Timeline.objects.create(
        autor = request.user,
        solicitacao_id = solicitar.id,
        descricao = f'{request.user.first_name} realizou a solicitação',
        lado = lado

    )
    solicitacoes = Solicitacoes.objects.all().exclude(status=3).order_by('-id')
    solicitacoes_paginators = Paginator(solicitacoes,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)

    return render(request,'ajax/tbl_solicitacoes.html',{'paginas':page})

@login_required(login_url='/')
def LineTimeline(request,codigo):
    itens = Timeline.objects.filter(solicitacao_id=codigo).all().order_by('-id')
    return render(request,'timeline.html',{'itens':itens})	
