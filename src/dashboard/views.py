from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from perfil.models import Perfil
@login_required(login_url='/')
def Dashboard(request):
    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    link_foto = foto.foto
    return render(request,'dashboard.html',{'foto':foto})