from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from perfil.models import Perfil
@login_required(login_url='/')
def Dashboard(request):
    foto =  Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = Perfil.objects.filter(user_profile_id = request.user.id).first()
    perm = perm.cargo
    link_foto = foto.foto
    if link_foto:
        pass
    else:
        link_foto = f"https://ui-avatars.com/api/?name={request.user.first_name}&color=7F9CF5&background=EBF4FF"
    return render(request,'dashboard.html',{'foto':foto,'perm':perm})