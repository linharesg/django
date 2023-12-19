from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name = "index"),
    # localhost:8000/1 -> ID do cliente -> Client 1 (Parâmetro da rota)
    path("<int:client_id>/", views.detail, name = "detail"), # Pasando parâmetro que é um numero inteiro. Sempre colocar o "/" no final da URL
    path("cadastro/", views.create, name="create"),
    path("<int:client_id>/atualizar", views.update, name="update"),
    path("<int:client_id>/remover/", views.delete, name="delete"),
]