from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def Solicitacoes(request):
    return render(request,'solicitacoes.html')

@login_required(login_url='/')
def Timeline(request):
    return render(request,'timeline.html')
