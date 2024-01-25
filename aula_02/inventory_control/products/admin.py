from django.contrib import admin
from .models import Products


# admin.site.register(Products)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sale_price", "is_perishable", "expiration_date", "enabled"]
    exclude = ["slug"]
    list_filter = ["name", "enabled", "is_perishable"]
    list_editable = ["sale_price", "is_perishable", "expiration_date"]
    exclude = ["thumbnail", "is_perishable", "slug"]