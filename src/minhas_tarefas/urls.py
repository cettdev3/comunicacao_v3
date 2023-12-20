from django.urls import include, path
from minhas_tarefas.views import Minhas_Tarefas,Show_Modal_Task,Concluir_Demanda

urlpatterns = [
    path('meus-jobs',  Minhas_Tarefas),
    path('ajax/show-modal-task',  Show_Modal_Task),
    path('ajax/concluir-demanda',  Concluir_Demanda),
    path('ajax/cadastrar-peca',  Concluir_Demanda),
]