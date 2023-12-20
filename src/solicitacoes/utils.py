
from .models import Solicitacoes,Timeline

def get_lado_timeline(id):
    ultimo_lado = Timeline.objects.filter(solicitacao_id=id).last()
    if ultimo_lado.lado == 1:
        return 2
    else:
        return 1
