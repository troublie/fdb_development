from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.test import TestCase
from django.urls import resolve

from ..views import pedido_detalhes
from ..models import Order, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Customer


class PedidoDetalhesTest(TestCase):
    def setUp(self):
        self.moeda = Moeda.objects.create(simbolo="USD", descricao="DOLAR")
        self.moeda = Moeda.objects.first()
        self.prioridade = Prioridade.objects.create(tipo="Alta")
        self.prioridade = Prioridade.objects.first()
        self.tipo_emb = Tipo_emb.objects.create(descricao="Spareparts")
        self.tipo_emb = Tipo_emb.objects.first()
        self.fornecedor = Fornecedor.objects.create(nome="Sojitz", endreco="Teste", email_contato="teste@gmail.com",
                                                    nome_contato="Joao")
        self.fornecedor = Fornecedor.objects.first()
        self.termo = Termo.objects.create(dias="30")
        self.termo = Termo.objects.first()
        self.customer = Customer.objects.create(nome="Jabil", endreco="Teste", email_contato="teste2@gmail.com",
                                                nome_contato="Joao")
        self.customer = Customer.objects.first()
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.user = User.objects.first()
        Order.objects.create(customer=self.customer, fornecedor=self.fornecedor, number='123', moeda=self.moeda,
                             amount_total='1200', responsavel_fdb=self.user, tipo_embarque=self.tipo_emb,
                             termo_pagto=self.termo, prioridade=self.prioridade)
        url = reverse_lazy('pedido_detalhes', kwargs={'pk': 1})
        self.response = self.client.get(url)

    def test_pedido_detalhes_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_pedido_detalhes_view_has_nav_links(self):
        home_url = reverse_lazy('home')
        consulta_pedido_url = reverse_lazy('lista_pedido')
        self.assertContains(self.response, home_url)
        self.assertContains(self.response, consulta_pedido_url)

    def test_pedido_detalhes_not_found_status_code(self):
        url = reverse_lazy('pedido_detalhes', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_pedido_detalhes_url_resolves_pedido_detalhes_view(self):
        view = resolve('/pedido_detalhes/1/')
        self.assertEquals(view.func, pedido_detalhes)
