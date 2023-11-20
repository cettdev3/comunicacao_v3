from django.urls import include, path
from minhas_tarefas.views import Minhas_Tarefas

urlpatterns = [
    path('meus-jobs',  Minhas_Tarefas),
]