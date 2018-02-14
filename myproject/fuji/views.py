from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Item


def home(request):
    return render(request, "home.html")


def consulta_pn(request):
    items = Item.objects.all()
    return render(request, "consulta_pn.html", {'items': items})


def item_detalhes(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_detalhes.html', {'item': item})
