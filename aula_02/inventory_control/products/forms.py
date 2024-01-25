from django import forms
from .models import Products
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
            "enabled": "Ativo"
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
