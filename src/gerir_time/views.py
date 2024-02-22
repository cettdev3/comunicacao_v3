from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from perfil.models import Perfil
from django.db import transaction

# Create your views here.
@login_required(login_url='/')
def Gerir_Time(request):
    usuarios = User.objects.all()
    for usuario in usuarios:
        perfil = Perfil.objects.filter(user_profile_id = usuario.id).first()
        usuario.perfil = perfil
        usuario.save()
    foto = Perfil.objects.filter(user_profile_id = request.user.id).first()
    return render(request,'gerir_time.html',{'usuarios':usuarios,'foto':foto})

@login_required(login_url='/')
def Cadastrar_Usuario(request):
    nome = request.POST.get('nome','')
    email = request.POST.get('email','')
    usuario = request.POST.get('usuario','')
    password = request.POST.get('password','')
    cargo = request.POST.get('cargo','')
    unidade = request.POST.get('unidade','')

    und_cadastrada = Perfil.objects.filter(und=unidade).first()
    if und_cadastrada and int(unidade) < 5:
        return JsonResponse({'erro': 'Não foi possível criar o usuário. A unidade já está vinculada a um outro usuário!'}, status=400)
    else:
        try:
            with transaction.atomic():
                usuario = User.objects.create(
                    username = usuario,
                    email = email,
                    first_name = nome,
                    password = password
                )
                perfil = Perfil.objects.create(
                    user_profile = usuario,
                    cargo = cargo,
                    und = unidade
                )
            
            usuarios = User.objects.all()
            for usuario in usuarios:
                perfil = Perfil.objects.filter(user_profile_id = usuario.id).first()
                usuario.perfil = perfil
                usuario.save()
            foto = Perfil.objects.filter(user_profile_id = request.user.id).first()
            return render(request,'ajax/tbl_usuarios.html',{'usuarios':usuarios,'foto': foto})
        except:
            return JsonResponse({'erro': 'Usuário ja existe!'}, status=400)

@login_required(login_url='/')
def Get_User(request):
    user_id = request.GET.get('user_id','')
    usuario = User.objects.filter(id = user_id).first()

    perfil = Perfil.objects.filter(user_profile_id = usuario.id).first()
    usuario.perfil = perfil

    return render(request,'ajax/tbl_usuarios.html',{'usuario':usuario})

@login_required(login_url='/')
def Alterar_Usuario(request):
    user_id = request.POST.get('user_id','')
    nome = request.POST.get('nome_modal','')
    email = request.POST.get('email_modal','')
    usuario = request.POST.get('usuario_modal','')
    password = request.POST.get('password_modal','')
    cargo = request.POST.get('cargo_modal','')
    unidade = request.POST.get('unidade_modal','')

    if unidade:
        und_cadastrada = Perfil.objects.filter(und=unidade).first()
    else:
        und_cadastrada = None

    if und_cadastrada and int(unidade) < 5 and und_cadastrada.user_profile_id != request.user.id:
        return JsonResponse({'erro': 'Não foi possível criar o usuário. A unidade já está vinculada a um outro usuário!'}, status=400)
    else:
        try:
            with transaction.atomic():
                usuario = User.objects.get(id=user_id)
                usuario.first_name = nome
                usuario.email = email
                if password:
                    usuario.password = password
                usuario.save()
                perf = Perfil.objects.filter(user_profile_id = usuario.id).first()
                if perf:
                    perf.cargo = cargo
                    perf.und = unidade
                    perf.save()

            usuarios = User.objects.all()
            for usuario in usuarios:
                perfil = Perfil.objects.filter(user_profile_id = usuario.id).first()
                usuario.perfil = perfil
                usuario.save()
            foto = Perfil.objects.filter(user_profile_id = request.user.id).first()
            return render(request,'ajax/tbl_usuarios.html',{'usuarios':usuarios,'foto': foto})
        except Exception as e:
            print(e)	
            return JsonResponse({'erro': 'Usuário ja existe!'}, status=400)