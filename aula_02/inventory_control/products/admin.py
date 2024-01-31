from django.contrib import admin
from .models import Products
from .models import Category
from .models import SupplierProduct


# admin.site.register(Products)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sale_price", "is_perishable", "expiration_date", "enabled"]
    list_filter = ["name", "enabled", "is_perishable"]
    list_editable = ["sale_price", "is_perishable", "expiration_date"]
    exclude = ["thumbnail", "is_perishable", "slug"]
    list_per_page = 100
    list_show_max_all = 1000

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    list_per_page = 100
    list_show_max_all = 1000
    
@admin.register(SupplierProduct)
class SupplierProduct(admin.ModelAdmin):
    list_display = ["id", "product", "cost_price"]
    search_fields = ["product"]
    list_per_page = 100
    list_max_show_all = 1000
    