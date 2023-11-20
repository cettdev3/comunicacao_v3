from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def Minhas_Tarefas(request):
    return render(request,'minhas_tarefas.html')