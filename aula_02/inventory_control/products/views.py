from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Products
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.

def index(request):
    products = Products.objects.order_by("-id")

    context = {"products": products}
    return render(request, "products/index.html", context)

@require_POST
def toggle_enabled(request, id):
    product = get_object_or_404(Products, pk=id)

    product.enabled = not product.enabled
    product.save()

    return JsonResponse({"message": "success"})