from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Solicitacoes

@login_required(login_url='/')
def Solicitacao(request):
    solicitacoes = Solicitacoes.objects.all()
    return render(request,'solicitacoes.html',{'solicitacoes':solicitacoes})

@login_required(login_url='/')
def Timeline(request):
    return render(request,'timeline.html')
