from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.create, name="create"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("categorias/<int:id>/delete", views.category_delete, name="category_delete"),
    path("search", views.search, name="search"),
    path("categorias/search", views.category_search, name="category_search"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("categorias/", views.category_index, name="category_index"), # se eu deixo essa linha por últmo (epois do update), não funciona. 404 (No Products matches the given query.)
    path("categorias/cadastro/", views.category_create, name="category_create"),
    path("<int:id>/delete_supplier", views.delete_supplier_from_product, name="delete_supplier"),
    path("<slug:slug>/", views.update, name="update"),
    path("categorias/<slug:slug>/", views.category_update, name="category_update"),
    path("<int:id>/suppliers/", views.get_suppliers_from_product, name="suppliers"),
]