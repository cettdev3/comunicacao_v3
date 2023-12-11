from django.urls import include, path
from solicitacoes.views import Solicitacao,LineTimeline,Paginar,Filter_Solicitacoes,Realizar_Solicitacao

urlpatterns = [
    path('solicitacoes',  Solicitacao),
    path('paginar',  Paginar),
    path('filter-solicitacoes',  Filter_Solicitacoes),
    path('realizar-solicitacao',  Realizar_Solicitacao),
    path('timeline/<codigo>',  LineTimeline)
]