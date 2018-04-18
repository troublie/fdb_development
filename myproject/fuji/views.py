from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order
from .forms import NewOrderForm, SearchForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")


def consulta_pn(request):
    items = Item.objects.all()
    return render(request, "consulta_pn.html", {'items': items})


def item_detalhes(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_detalhes.html', {'item': item})

@login_required
def cadastro_pedido(request):
    #user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.responsavel_fdb = request.user
            order.save()
            return redirect('pedido_detalhes', pk=order.pk)  # TODO: redirect to the created PO.
    else:
        form = NewOrderForm()
    return render(request, 'cadastro_pedido.html', {'form': form})


def lista_pedido(request):
    form = SearchForm()
    orders = Order.objects.all()
    return render(request, "lista_pedido.html", {'orders': orders, 'form': form})


def pedido_detalhes(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'pedido_detalhes.html', {'order': order})

def resultados(request):
    return render()