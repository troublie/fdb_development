from django.shortcuts import render
from .models import Item


def home(request):
    return render(request, "home.html")


def consulta_pn(request):
    items = Item.objects.all()
    return render(request, "consulta_pn.html", {'items': items})
