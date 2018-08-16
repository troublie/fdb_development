from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase
from ..views import search
from ..models import Customer, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Order


class SearchViewTest(TestCase):
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
        url = reverse_lazy('search')
        self.response = self.client.get(url, {'q': '123'})

    def test_search_list_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_search_list_view_has_link_to_homepage(self):
        url_homepage = reverse_lazy('home')
        self.assertContains(self.response, url_homepage)

    def test_view_search_url_resolve_search_view(self):
        view = resolve('/search/')
        self.assertEquals(view.func, search)

    def test_search_view_show_ok_results_from_db_by_columns(self):
        self.assertContains(self.response, '<td>', 8)

    def test_search_view_contains_link_to_order(self):
        pedido_detalhes_url = reverse_lazy('pedido_detalhes', kwargs={"pk": Order.objects.all().first().pk})
        self.assertContains(self.response, 'href="{0}"'.format(pedido_detalhes_url))
