from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Products, SupplierProduct
from .models import Category
from .forms import ProductsForm, SupplierProductFormSet
from .forms import CategoryForms
from django.urls import reverse

def index(request):
    products = Products.objects.order_by("-id")
    paginator = Paginator(products, 2)
    #/fornecedores?page=1
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj,}
    return render(request, "products/index.html", context)

def search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:index")
    
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

def category_search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:category_index")
    
    # O "Q" é usado para combinar filtros (AND (&) ou | (OR))
    categories = Category.objects \
        .filter(Q(name__icontains=search_value) | 
            Q(description__icontains=search_value)) \
        .order_by("-id")

    paginator = Paginator(categories, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "categories": page_obj}

    return render(request, "categories/index.html", context)

def create(request):

    form_action = reverse("products:create")
    
    if request.method == "POST":

        form = ProductsForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save()

            supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)

            if supplier_product_formset.is_valid():
                supplier_product_formset.save()
                messages.success(request, "O produto foi cadastrado com sucesso!")
            else:
                messages.error(request, "Falha ao cadastrar os fornecedores do produto.")
                product.delete()

                supplier_product_formset = SupplierProductFormSet(request.POST)

                context = { "form": form, "supplier_product_formset": supplier_product_formset, "form_action": form_action }
                return render(request, "products/create.html", context)
            
            return redirect ("products:index")

        print(form.errors)
        
        messages.error(request, "Falha ao cadastrar o produto. Verifique o preenchimento dos campos.")
        
        supplier_product_formset = SupplierProductFormSet(request.POST)

        context = { "form": form, "supplier_product_formset": supplier_product_formset, "form_action": form_action }
        return render(request, "products/create.html", context)
    
    #GET
    form = ProductsForm()

    supplier_product_formset = SupplierProductFormSet()

    context = { "form": form, "supplier_product_formset": supplier_product_formset, "form_action": form_action }

    
    return render(request, "products/create.html", context)

def category_create(request):
    
    form_action = reverse("products:category_create")

    if request.method == "POST":
        
        form = CategoryForms(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Categoria criada com sucesso!")

            return redirect("products:category_index")

        messages.error(request, "Falha ao cadastrar a categoria. Verifique os campos preenchidos.")

        context = { "form": form, "form_action": form_action }
        return render(request, "categories.create.html", context)

    #GET
    form = CategoryForms()

    context = {"form": form, "form_action": form_action}

    return render(request, "categories/create.html", context)
    
def update(request, slug):
    product = get_object_or_404(Products, slug=slug)
    form_action = reverse("products:update", args=(slug,))

    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES, instance=product)
        supplier_product_formset = SupplierProductFormSet(
            request.POST, instance=product)

        if form.is_valid():
            try:
                if form.cleaned_data["photo"] is False:
                    product.thumbnail.delete(save=False)

                form.save()

                print(supplier_product_formset.data)
                print(supplier_product_formset.errors)
                
                if supplier_product_formset.is_valid():
                    supplier_product_formset.save()
                    messages.success(request, "Produto atualizado com sucesso")
                    return redirect("products:index")
                else:
                    messages.error(
                        request, "Falha ao atualizar o produto - Formulário de fornecedores inválido.")

            except IntegrityError:
                messages.error(
                    request, "Falha ao atualizar o produto - Não é possível ter o mesmo fornecedor para o mesmo produto mais de uma vez.")
        else:
            messages.error(
                request, "Falha ao atualizar o produto - Formulário inválido.")
        
        
        supplier_product_formset = SupplierProductFormSet(instance=product)
        context = {
            "form_action": form_action,
            "form": form,
            "supplier_product_formset": supplier_product_formset
        }
        
        return render(request, "products/create.html", context)


    form = ProductsForm(instance=product)
    supplier_product_formset = SupplierProductFormSet(instance=product)

    context = {
        "form_action": form_action,
        "form": form,
        "supplier_product_formset": supplier_product_formset
    }

    return render(request, "products/create.html", context)

def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form_action = reverse("products:category_update", args=(slug,)) # Obtendo a URL da rota de atualização

    
    if request.method == "POST":
        form = CategoryForms(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")

            return (redirect("products:category_index"))
        
        context = {
            "form_action": form_action,
            "form": form
        }
        
        return render(request, "categories/create.html", context) 
        
    # GET
    form = CategoryForms(instance=category)
    
    context = {
        "form_action": form_action,
        "form": form,
    }

    return render(request, "categories/create.html", context)

def category_index(request):
    categories = Category.objects.order_by("-id")
    
    paginator = Paginator(categories, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "categories": page_obj }
    return render(request, "categories/index.html", context)

# só permite que a view seja acessada através de POST, e não de GET
@require_POST
def delete(request, id):
    product = get_object_or_404(Products, pk=id)
    product.delete()

    return redirect("products:index")

@require_POST
def category_delete(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()

    return redirect("products:category_index")

@require_POST
# def toggle_enabled(request, id):
def toggle_enabled(request, id):
    product = get_object_or_404(Products, pk=id)

    product.enabled = not product.enabled
    product.save()
    
    return JsonResponse({ "message": "success"})

@require_GET
def get_suppliers_from_product(request, id):
    suppliers = SupplierProduct.objects.filter(product__id=id).order_by("-id")
    
    # Serialização
    suppliers_serialized = [{
        "id": supplierProduct.id,
        "name": supplierProduct.supplier.fantasy_name,
        "cost_price": supplierProduct.cost_price

    } for supplierProduct in suppliers]

    return JsonResponse(suppliers_serialized, safe = False)

@require_POST
def delete_supplier_from_product(request, id):
    supplier_product = get_object_or_404(SupplierProduct, pk=id)
    supplier_product.delete()

    return JsonResponse({ "message": "success"})