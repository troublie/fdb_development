from django import forms
from django.forms import DateInput, DateField
from django.utils import translation

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



