from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .models import Item, Order
from .forms import NewOrderForm, SearchForm, DateForm, UpdateOrderForm
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
    # user = User.objects.first()  # TODO: get the currently logged in user
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
    date_form = DateForm()
    orders = Order.objects.all()
    return render(request, "lista_pedido.html", {'orders': orders, 'form': form, 'date_form': date_form})


def pedido_detalhes(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'pedido_detalhes.html', {'order': order})


def search(request):
    form = SearchForm()
    date_form = DateForm()
    q = request.GET.get('q')
    orders = Order.objects.filter(number__contains=q)
    return render(request, "lista_pedido.html", {'orders': orders, 'form': form, 'date_form': date_form})


def filter(request):
    form = SearchForm()
    date_form = DateForm()
    init_date = request.GET.get('init_date')
    end_date = request.GET.get('end_date')
    orders = Order.objects.filter(created_at__range=(init_date, end_date))
    return render(request, "lista_pedido.html", {'orders': orders, 'form': form, 'date_form': date_form})


@method_decorator(login_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    #fields = ('date_sent_vendor', 'proforma', 'invoice', 'instrucoes', 'embarcado_finalizado_em', 'awb', 'tracking',
              #'amount_total', 'tipo_embarque', 'termo_pagto', 'pago', 'prioridade',)
    form_class = UpdateOrderForm
    template_name = 'edit_order.html'
    pk_url_kwarg = 'order_pk'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(responsavel_fdb=self.request.user)

    def form_valid(self, form):
        order = form.save(commit=False)
        order.updated_by = self.request.user
        order.last_update = timezone.now()
        order.save()
        return redirect('pedido_detalhes', pk=order.pk)
