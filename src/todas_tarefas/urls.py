from django.urls import include, path
from todas_tarefas.views import Todas_Tarefas,Get_Users_Designante,Get_Peca_Filter,Get_Modal_task,Jobs_Individual,Get_Pecas,Get_Pecas_Individual

urlpatterns = [
    path('todos-jobs',  Todas_Tarefas),
    path('ajax/get-users-designante',  Get_Users_Designante),
    path('ajax/get-peca-filter',  Get_Peca_Filter),
    path('ajax/modal-task',  Get_Modal_task),
    path('jobs-individual',  Jobs_Individual),
    path('ajax/get-pecas',  Get_Pecas),
    path('ajax/get-peca-filter-individual', Get_Pecas_Individual),

]