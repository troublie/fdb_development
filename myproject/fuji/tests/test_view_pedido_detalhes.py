from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.test import TestCase
from django.urls import resolve

from ..views import pedido_detalhes
from ..models import Order, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Customer


class PedidoDetalhesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.moeda = Moeda.objects.create(simbolo="USD", descricao="DOLAR")
        cls.moeda = Moeda.objects.first()
        cls.prioridade = Prioridade.objects.create(tipo="Alta")
        cls.prioridade = Prioridade.objects.first()
        cls.tipo_emb = Tipo_emb.objects.create(descricao="Spareparts")
        cls.tipo_emb = Tipo_emb.objects.first()
        cls.fornecedor = Fornecedor.objects.create(nome="Sojitz", endreco="Teste", email_contato="teste@gmail.com",
                                                   nome_contato="Joao")
        cls.fornecedor = Fornecedor.objects.first()
        cls.termo = Termo.objects.create(dias="30")
        cls.termo = Termo.objects.first()
        cls.customer = Customer.objects.create(nome="Jabil", endreco="Teste", email_contato="teste2@gmail.com",
                                               nome_contato="Joao")
        cls.customer = Customer.objects.first()
        cls.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        cls.user = User.objects.first()
        Order.objects.create(customer=cls.customer, fornecedor=cls.fornecedor, number='123', moeda=cls.moeda,
                             amount_total='1200', responsavel_fdb=cls.user, tipo_embarque=cls.tipo_emb,
                             termo_pagto=cls.termo, prioridade=cls.prioridade)

    def setUp(self):
        url = reverse_lazy('pedido_detalhes', kwargs={'pk': Order.objects.all().first().pk})
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
