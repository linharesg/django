from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Client
# Create your views here.
def index(request):
    clients = Client.objects.all()

    context = {
        "clients": clients
    }
    return render(request, 'index.html', context)

def detail(request, client_id):
    client = get_object_or_404(Client, pk = client_id)

    context = {
        "client": client
    }

    return render(request, 'detail.html', context)

def create(request):
    return HttpResponse("Criação")

def update(request, client_id):
    return HttpResponse(f"Edição: {client_id}")

def delete(request, client_id):
    return HttpResponse(f"Remover: {client_id}")