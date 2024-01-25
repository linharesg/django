from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Products
from .forms import ProductsForm
from django.urls import reverse

def index(request):
    products = Products.objects.order_by("-id")
    
    paginator = Paginator(products, 2)
    #/fornecedores?page=1
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj }
    return render(request, "products/index.html", context)

def search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:index")
    
    #Filtrando os fornecedores
    # products = Products.objects.filter(fantasy_name__icontains=search_value)

    # O "Q" é usado para combinar filtros (AND (&) ou | (OR))
    products = Products.objects \
        .filter(Q(name__icontains=search_value) | 
            Q(description__icontains=search_value) |
            Q(category__name__icontains=search_value)) \
        .order_by("-id")

    paginator = Paginator(products, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj}

    return render(request, "products/index.html", context)

def create(request):
    
    form_action = reverse("products:create")
    
    if request.method == "POST":
        form_action = reverse("products:create")

        if request.method == 'POST':
            form = ProductsForm(request.POST, request.FILES)
        
            if form.is_valid():
                form.save()
                
                messages.success(request, "O produto foi cadastrado com sucesso!")
                
                return redirect ("products:index")
            # print(form.errors)
        
        messages.error(request, "Falha ao cadastrar o produto. Verifique o preenchimento dos campos.")
        
        context = { "form": form, "form_action": form_action }
        
        return render(request, "products/create.html", context)
    
    #GET
    form = ProductsForm()
    
    context = { "form": form, "form_action": form_action }
    
    return render(request, "products/create.html", context)

def update(request, slug):
    product = get_object_or_404(Products, slug=slug)
    form_action = reverse("products:update", args=(slug,)) # Obtendo a URL da rota de atualização

    
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            if ProductsForm(request.POST, request.FILES, instance=product):
                product.thumbnail.delete(save=False)

            form.save()
            messages.success(request, "Produto atualizado com sucesso!")

            return (redirect("products:index"))
        
        context = {
            "form_action": form_action,
            "form": form
        }
        
        return render(request, "products/create.html", context) 
        
    # GET
    form = ProductsForm(instance=product)
    
    context = {
        "form_action": form_action,
        "form": form,
    }

    return render(request, "products/create.html", context)

# só permite que a view seja acessada através de POST, e não de GET
@require_POST
def delete(request, id):
    product = get_object_or_404(Products, pk=id)
    product.delete()

    return redirect("products:index")

@require_POST
# def toggle_enabled(request, id):
def toggle_enabled(request, id):
    product = get_object_or_404(Products, pk=id)

    product.enabled = not product.enabled
    product.save()
    
    return JsonResponse({ "message": "success"})