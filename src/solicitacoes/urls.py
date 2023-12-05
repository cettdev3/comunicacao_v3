from django.urls import include, path
from solicitacoes.views import Solicitacao,Timeline,Paginar,Filter_Solicitacoes

urlpatterns = [
    path('solicitacoes',  Solicitacao),
    path('paginar',  Paginar),
    path('filter-solicitacoes',  Filter_Solicitacoes),
    path('timeline',  Timeline)
]