from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        
        error_messages = {
            "company_name": {
                "unique": "A razão social já existe"
            }
        }