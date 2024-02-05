from django.urls import path
from . import views
from .views import SupplierListView, SupplierSearchView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView
app_name = "suppliers"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", SupplierListView.as_view(), name="index"),
    # path("cadastro/", views.create, name="create"),
    path("cadastro/", SupplierCreateView.as_view(), name="create"),
    # path("<int:id>/delete", views.delete, name="delete"),
    path("<int:pk>/delete", SupplierDeleteView.as_view(), name="delete"),
    # path("search", views.search, name="search"),
    path("search", SupplierSearchView.as_view(), name="search"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    # path("<slug:slug>/", views.update, name="update"),
    path("<slug:slug>/", views.SupplierUpdateView.as_view(), name="update"),
]