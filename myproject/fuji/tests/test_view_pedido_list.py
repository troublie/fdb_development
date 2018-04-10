from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase
from ..views import lista_pedido
from ..models import Customer, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Order


class PedidoListViewTest(TestCase):
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
        url = reverse_lazy('lista_pedido')
        self.response = self.client.get(url)

    def test_pedido_list_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_pedido_list_view_has_link_to_homepage(self):
        url_homepage = reverse_lazy('home')
        self.assertContains(self.response, url_homepage)

    def test_lista_pedido_url_resolve_lista_pedido_view(self):
        view = resolve('/lista_pedido/')
        self.assertEquals(view.func, lista_pedido)

    def test_lista_pedido_view_show_ok_results_from_db_by_columns(self):
        self.assertContains(self.response, '<td>', 8)

    def test_lista_pedido_view_contains_link_to_order(self):
        self.assertContains(self.response, 'a href="/pedido_detalhes/1/"')
