from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Supplier
from .forms import SupplierForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView,  DetailView, CreateView, UpdateView, DeleteView

class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/index.html"
    paginate_by = 1
    ordering = "-id"
    # Escrito dessa forma, substitui a view "index" que tinha sido criada antes
    
class SupplierSearchView(ListView):
    model = Supplier
    template_name = "suppliers/index.html"
    paginate_by = 1
    # ordering = "-id" Ordenação deve ser feita direto no queryset pois houve sobreescrita de queryset

    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if not search_value:
            return Supplier.objects.all().order_by("-id")
       
        return Supplier.objects.filter(
                                    Q(fantasy_name__icontains=search_value) | 
                                    Q(company_name__icontains=search_value)).order_by("-id")

class SupplierCreateView(CreateView):
    model = Supplier
    template_name = "suppliers/create.html"
    form_class = SupplierForm
    success_url = reverse_lazy("suppliers:index")
    
    def form_valid(self, form):
        
        # Save no banco de dados colocado antes da mensage, porque caso dê algum erro na hora de salvar, vai esoturar exceção e não vai mostrar a mensagem de sucesso
        response = super().form_valid(form)
        messages.success(self.request, "Fornecedor cadastrado com sucesso!")
        return response
    
    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_action"] = reverse("suppliers:create")
        return context


class SupplierUpdateView(UpdateView):
    model = Supplier
    template_name = "suppliers/update.html"
    form_class = SupplierForm
    success_url = reverse_lazy("suppliers:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Fornecedor atualizado com sucesso!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.success(self.request, "Erro ao atualizar o fornecedor!")
        return response

def update(request, slug):
    supplier = get_object_or_404(Supplier, slug=slug)
    form_action = reverse("suppliers:update", args=(slug,)) # Obtendo a URL da rota de atualização

    
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            messages.success(request, "Fornecedor atualizado com sucesso!")

            return (redirect("suppliers:index"))
        
        context = {
            "form_action": form_action,
            "form": form
        }
        
        return render(request, "suppliers/create.html", context) 
        
    # GET
    form = SupplierForm(instance=supplier)
    
    context = {
        "form_action": form_action,
        "form": form,
    }

    return render(request, "suppliers/create.html", context)

class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy("suppliers:index")

# só permite que a view seja acessada através de POST, e não de GET
@require_POST
# def toggle_enabled(request, id):
def toggle_enabled(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    supplier.enabled = not supplier.enabled
    supplier.save()
    
    return JsonResponse({ "message": "success"})