from django.urls import include, path
from todas_tarefas.views import Todas_Tarefas

urlpatterns = [
    path('todos-jobs',  Todas_Tarefas),
]