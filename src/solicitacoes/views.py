from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Solicitacoes
from django.core.paginator import Paginator

def convert_data_formatada(data):

    data = data.split('/')
    data = data[2]+'-'+data[1]+'-'+data[0]
    return data

@login_required(login_url='/')
def Solicitacao(request):
    solicitacoes = Solicitacoes.objects.all().exclude(status=3)
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

@login_required(login_url='/')
def Timeline(request):
    return render(request,'timeline.html')
