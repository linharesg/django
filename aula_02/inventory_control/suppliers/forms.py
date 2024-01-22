from django import forms
from .models import Supplier
import re

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        
        error_messages = {
            "fantasy_name": {
                "unique": "A razão social já existe.",
                "max_length": "Limite de 255 caracteres."
            }
        }
    
    # clean_<nome_campo>. esse é o padrão do django. se usar outro nome pra função, não funciona
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj", "")
        
        # Removendo valores não numéricos
        cnpj = re.sub("[^0-9]", "", cnpj)

        return cnpj

    def clean_phone(self):
        
        phone = self.cleaned_data.get("phone", "")
        print(f"cleande_data: {phone}")
        # Removendo valores não numéricos
        phone = re.sub("[^0-9]", "", phone)

        print(f"regex: {phone}")
        return phone

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get("zipcode", "")
        
        # Removendo valores não numéricos
        zipcode = re.sub("[^0-9]", "", zipcode)

        return zipcode
        