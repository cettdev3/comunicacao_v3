from django.urls import include, path
from solicitacoes.views import Solicitacoes,Timeline

urlpatterns = [
    path('solicitacoes',  Solicitacoes),
    path('timeline',  Timeline)
]