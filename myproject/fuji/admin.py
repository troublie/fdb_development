from django.contrib import admin
from .models import Item, Order, Moeda, Tipo_emb, Fornecedor, Termo, Customer, Prioridade

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Moeda)
admin.site.register(Tipo_emb)
admin.site.register(Fornecedor)
admin.site.register(Termo)
admin.site.register(Customer)
admin.site.register(Prioridade)


