from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from django.views.decorators.http import require_POST

def index(request):
    suppliers = Supplier.objects.order_by("-id")
    context = { "suppliers": suppliers }
    return render(request, "index.html", context)

# só permite que a view seja acessada através de POST, e não de GET
@require_POST
def delete(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    supplier.delete()

    return redirect("suppliers:index")