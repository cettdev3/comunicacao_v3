from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Demandas,Solicitacoes,Pecas,Perfil
from django.contrib.auth.models import User
from django.http import JsonResponse
from repositorio.models import Arquivos_Demandas
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='/')
def Todas_Tarefas(request):
    demandas = Demandas.objects.all()
    solicitacoes = Solicitacoes.objects.all()
    usuarios = User.objects.all()
    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = foto.cargo
    return render(request,'todas_tarefas.html',{'demandas':demandas,'solicitacoes':solicitacoes,'usuarios':usuarios,'foto':foto,'perm':perm})

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
        foto =  Perfil.objects.filter(user_profile_id = demandas.autor_id).first()
        perm = Perfil.objects.filter(user_profile_id =request.user.id).first()
        return render(request, 'ajax/modal_task.html', {'demanda': demandas,'perm':perm})
       
    else:
        return JsonResponse({"error_message": "Solicitação Devolvida!"}, status=400)
    

@login_required(login_url='/')
def Jobs_Individual(request):
    demandas = Demandas.objects.filter(designante_id = request.user.id).all()
    demandas_list = []
    demandas_append = []
    for demanda in demandas:
        print(demanda.peca.solicitacao.titulo)
        if demanda.peca.solicitacao.titulo not in demandas_append:
            demandas_append.append( demanda.peca.solicitacao.titulo)
            demandas_list.append(demanda)
    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = foto.cargo
    return render(request,'jobs_individuais.html',{'demandas':demandas,'demandas_list':demandas_list,'foto':foto,'perm':perm})

@login_required(login_url='/')
def Get_Pecas(request):
    solicitacao_id = request.GET.get('solicitacao_id',"")
    if solicitacao_id:
        pecas = Pecas.objects.filter(solicitacao_id = solicitacao_id).all()
    else:
        pecas =[]
    return render(request,'ajax/ajax_get_pecas.html',{'pecas':pecas})

@login_required(login_url='/')
def Get_Pecas_Individual(request):
    peca = request.GET.get('peca_id','')
    solicitacao = request.GET.get('solicitacao_id','')
    if peca:
        demandas = Demandas.objects.filter(peca_id=peca,designante_id = request.user.id).all()

    else:
        demandas = Demandas.objects.filter(designante_id=request.user.id,peca_id__solicitacao_id=solicitacao).all(
            
        )
    return render(request, 'ajax/ajax_tbl_demandas.html', {'demandas': demandas})

def All_Jobs(request):
    solicitacoes = Solicitacoes.objects.all().order_by('-id')
    for solicitacao in solicitacoes:
        perfil = Perfil.objects.filter(user_profile_id=solicitacao.autor_id).first()
        solicitacao.perfil = perfil
    solicitacoes_paginators = Paginator(solicitacoes,50)
    page_num = request.GET.get('pagina')
    page = solicitacoes_paginators.get_page(page_num)
    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = foto.cargo
    return render(request,'todos_jobs.html',{'paginas':page,'solicitacoes':solicitacoes,'foto':foto,'perm':perm})