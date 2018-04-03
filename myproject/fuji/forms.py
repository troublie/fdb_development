from django import forms
from .models import Order


class NewOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['customer', 'received_date', 'fornecedor', 'date_sent_vendor',
                  'number', 'proforma', 'invoice', 'instrucoes', 'embarcado_finalizado_em',
                  'awb', 'tracking', 'moeda', 'amount_total', 'responsavel_fdb', 'tipo_embarque',
                  'termo_pagto', 'vencimento', 'pago', 'prioridade'
                  ]
