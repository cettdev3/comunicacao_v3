from django.urls import include, path
from repositorio.views import Repositorio

urlpatterns = [
    path('repositorio',  Repositorio),
]