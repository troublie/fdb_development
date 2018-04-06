from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    pn = models.CharField(max_length=18, unique=True)
    designChange = models.CharField(max_length=2, blank=False, null=True)
    partName = models.CharField(max_length=80, blank=False, null=True)
    partNamePort = models.CharField(max_length=80, blank=True, null=True)
    rating = models.CharField(max_length=80, blank=True, null=True)
    remark = models.CharField(max_length=80, blank=True, null=True)
    information = models.CharField(max_length=80, blank=True, null=True)
    yenPrice = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    ncm = models.CharField(max_length=8, blank=True, null=True)
    finalidade = models.CharField(max_length=500, blank=True, null=True)
    material = models.CharField(max_length=80, blank=True, null=True)
    comentarios = models.CharField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=True)

    def __str__(self):
        return self.pn


class Moeda(models.Model):
    simbolo = models.CharField(max_length=3, unique=True)
    descricao = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.simbolo


class Prioridade(models.Model):
    tipo = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.tipo


class Tipo_emb(models.Model):
    descricao = models.CharField(max_length=30, unique=True, blank=False)

    def __str__(self):
        return self.descricao


class Fornecedor(models.Model):
    nome = models.CharField(max_length=80, unique=True, blank=False)
    endreco = models.CharField(max_length=200, unique=True, blank=False)
    email_contato = models.EmailField(max_length=60, unique=True, blank=False)
    nome_contato = models.CharField(max_length=60, unique=False, blank=False)

    def __str__(self):
        return self.nome


class Termo(models.Model):
    dias = models.DecimalField(max_digits=3, decimal_places=0, null=False, blank=False)

    def __str__(self):
        return str(self.dias)


class Customer(models.Model):
    nome = models.CharField(max_length=80, unique=True, blank=False)
    endreco = models.CharField(max_length=400, unique=True, blank=False)
    email_contato = models.EmailField(max_length=60, unique=True, blank=False)
    nome_contato = models.CharField(max_length=60, unique=False, blank=False)

    def __str__(self):
        return self.nome

class Order(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True, verbose_name='Criado em')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders", blank=False, verbose_name='Cliente')
    received_date = models.DateField(blank=True, null=True, verbose_name='Data recebida')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name="orders", verbose_name='Fornecedor')
    date_sent_vendor = models.DateField(blank=True, null=True, verbose_name='Data de envio ao fornecedor')
    number = models.CharField(max_length=30, unique=True, blank=False,verbose_name='Número')
    proforma = models.CharField(max_length=30, blank=True, null=True, verbose_name='Proforma Invoice')
    invoice = models.CharField(max_length=30, blank=True, null=True,verbose_name='Invoice')
    instrucoes = models.CharField(max_length=30, blank=True, null=True, verbose_name='Instruções de embarque')
    embarcado_finalizado_em = models.DateField(blank=True, null=True, verbose_name='Embarcado/Finalizado em')
    awb = models.CharField(max_length=30, blank=True, null=True, verbose_name='AWB')
    tracking = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tracking')
    moeda = models.ForeignKey(Moeda, on_delete=models.PROTECT, related_name="orders", blank=False, null=False, verbose_name='Moeda')
    amount_total = models.DecimalField(max_digits=16, decimal_places=0, null=False, blank=False, verbose_name='Total')
    responsavel_fdb = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="orders", verbose_name='Responsável')
    tipo_embarque = models.ForeignKey(Tipo_emb, null=False, on_delete=models.PROTECT, blank=False, related_name="orders", verbose_name='Tipo')
    termo_pagto = models.ForeignKey(Termo, null=False, on_delete=models.PROTECT, blank=False, related_name="orders", verbose_name='Termo de Pagamento')
    vencimento = models.DateField(blank=True, null=True, verbose_name='Vencimento')
    pago = models.NullBooleanField(blank=True, verbose_name='Pago?')
    last_update = models.DateField(auto_now_add=True, verbose_name='Última atualização em')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="+", verbose_name='Última atualização por')
    prioridade = models.ForeignKey(Prioridade, null=False, on_delete=models.PROTECT, blank=False, related_name="orders", verbose_name='Prioridade')

    def __str__(self):
        return self.number



