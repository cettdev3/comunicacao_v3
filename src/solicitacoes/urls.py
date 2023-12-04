from django.urls import include, path
from solicitacoes.views import Solicitacao,Timeline

urlpatterns = [
    path('solicitacoes',  Solicitacao),
    path('timeline',  Timeline)
]