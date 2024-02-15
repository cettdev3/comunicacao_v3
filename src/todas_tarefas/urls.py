from django.urls import include, path
from todas_tarefas.views import Todas_Tarefas,Get_Users_Designante,Get_Peca_Filter

urlpatterns = [
    path('todos-jobs',  Todas_Tarefas),
    path('ajax/get-users-designante',  Get_Users_Designante),
    path('ajax/get-peca-filter',  Get_Peca_Filter),

]