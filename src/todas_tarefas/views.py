from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def Todas_Tarefas(request):
    return render(request,'todas_tarefas.html')