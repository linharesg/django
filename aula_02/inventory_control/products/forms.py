from django import forms
from .models import Products
from .models import Category
import re

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        # fields = "__all__"
        exclude = ["thumbnail", "slug", "is_perishable"]
        
        labels = {
            "name": "Nome",
            "description": "Descrição",
            "sale_price": "Preço de venda",
            "expiration_date": "Data de expiração",
            "photo": "Imagem do produto",
            "enabled": "Ativo",
            "category": "Categoria",
        }
        
        error_messages = {
            "name": {
                "required": "O campo nome é obrigatório",
                "unique": "Já existe um produto cadastrado com esse nome"
            },
            "description": {
                "required": "O campo descrição é obrigatório."
            },
            "sale_price": {
                "required": "O preço é obrigatório."
            },
        }
        
        
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
            }

class CategoryForms(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = "__all__"
        
        labels = {
            "name": "Nome da categoria",
            "description": "Descrição da categoria",
        }