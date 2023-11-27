from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def Repositorio(request):
    return render(request,'repositorio.html')