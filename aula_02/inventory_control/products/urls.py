from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
]