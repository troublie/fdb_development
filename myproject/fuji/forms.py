from django import forms
from django.forms import DateInput


from .models import Order

class DateInput(forms.DateInput):
    input_type = 'date'

class NewOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['customer', 'received_date', 'fornecedor', 'date_sent_vendor',
                  'number', 'proforma', 'invoice', 'instrucoes', 'embarcado_finalizado_em',
                  'awb', 'tracking', 'moeda', 'amount_total', 'responsavel_fdb', 'tipo_embarque',
                  'termo_pagto', 'vencimento', 'pago', 'prioridade'
                  ]
        widgets = {
            'received_date': DateInput(),
            'date_sent_vendor': DateInput(),
            'embarcado_finalizado_em': DateInput()
        }

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100)

    class Meta:
        fields = ['q']



