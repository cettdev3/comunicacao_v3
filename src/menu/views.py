from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Notificacoes
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from django.db import transaction
