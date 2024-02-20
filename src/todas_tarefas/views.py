from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Demandas,Solicitacoes
from django.contrib.auth.models import User
from django.http import JsonResponse
from repositorio.models import Arquivos_Demandas

# Create your views here.
@login_required(login_url='/')
def Todas_Tarefas(request):
    demandas = Demandas.objects.all()
    solicitacoes = Solicitacoes.objects.all()
    usuarios = User.objects.all()
    return render(request,'todas_tarefas.html',{'demandas':demandas,'solicitacoes':solicitacoes,'usuarios':usuarios})

@login_required(login_url='/')
def Get_Users_Designante(request):
    solicitacao_id = request.GET.get('solicitacao_id')
    if solicitacao_id:
        usuarios_list = []
        users_apend = []
        usuarios = Demandas.objects.filter(peca__solicitacao=solicitacao_id).all()
        for usuario in usuarios:
            if usuario.designante_id not in users_apend:
                users_apend.append(usuario.designante_id)
                usuarios_list.append(usuario)
    else:
        usuarios_list = []
    return render(request, 'ajax/ajax_designante.html', {'usuarios': usuarios_list})

@login_required(login_url='/')
def Get_Peca_Filter(request):
    solicitacao_id = request.GET.get('solicitacao_id')
    designante_id = request.GET.get('designante')
    if solicitacao_id:
        if designante_id:
            demandas = Demandas.objects.filter(peca__solicitacao=solicitacao_id,designante_id=designante_id).all()
        else:
            demandas = Demandas.objects.filter(peca__solicitacao=solicitacao_id).all()
    else:
        demandas = Demandas.objects.all()
    return render(request, 'ajax/ajax_tbl_demandas.html', {'demandas': demandas})

@login_required(login_url='/')
def Get_Modal_task(request):
    demanda_id = request.GET.get('demanda_id')
    
    if demanda_id:
        demandas = Demandas.objects.filter(id=demanda_id).first()
        arquivos_demandas = Arquivos_Demandas.objects.filter(demanda_id=demanda_id).all()
        demandas.arquivos_demandas = arquivos_demandas
        return render(request, 'ajax/modal_task.html', {'demanda': demandas})
       
    else:
        return JsonResponse({"error_message": "Solicitação Devolvida!"}, status=400)
    