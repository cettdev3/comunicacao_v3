from django.urls import include, path
from minhas_tarefas.views import Minhas_Tarefas,Show_Modal_Task,Concluir_Demanda,Cadastrar_Peca,Designar_Usuário,alterarSolicitacao,devolveSolicitacao,showDemandaModal

urlpatterns = [
    path('meus-jobs',  Minhas_Tarefas),
    path('ajax/show-modal-task',  Show_Modal_Task),
    path('ajax/concluir-demanda',  Concluir_Demanda),
    path('ajax/cadastrar-peca',  Cadastrar_Peca),
    path('ajax/designar-usuario',  Designar_Usuário),
    path('ajax/altera-solicitacao',  alterarSolicitacao),
    path('ajax/devolve-solicitacao',  devolveSolicitacao),
    path('ajax/show-demanda-task',  showDemandaModal),
]