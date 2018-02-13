from django.http import Http404
from django.shortcuts import render
from .models import Item


def home(request):
    return render(request, "home.html")


def consulta_pn(request):
    items = Item.objects.all()
    return render(request, "consulta_pn.html", {'items': items})


def item_detalhes(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        raise Http404
    return render(request, 'item_detalhes.html', {'item': item})
