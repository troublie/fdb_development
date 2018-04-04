from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase

from ..forms import NewOrderForm
from ..views import home, consulta_pn, item_detalhes, cadastro_pedido
from ..models import Item


class HomeTests(TestCase):

    def setUp(self):
        url = reverse_lazy('signup')
        data = {
            'username': 'john',
            'email': 'john@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        url = reverse_lazy('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_consulta_pn_page(self):
        consulta_pn_url = reverse_lazy('consulta_pn')
        self.assertContains(self.response, 'href="{0}"'.format(consulta_pn_url))

    def test_home_view_contains_link_to_cadastro_po_page(self):
        cadastro_pedido_url = reverse_lazy('cadastro_pedido')
        self.assertContains(self.response, 'href="{0}"'.format(cadastro_pedido_url))


class ItemListTests(TestCase):
    def setUp(self):
        Item.objects.create(pn="A5053C", partName="ORING")
        url = reverse_lazy('consulta_pn')
        self.response = self.client.get(url)

    def test_itemList_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_itemList_url_resolves_itemList_view(self):
        view = resolve('/consulta_pn/')
        self.assertEquals(view.func, consulta_pn)

    def test_item_detalhes_view_success_stauts_code(self):
        url = reverse_lazy('item_detalhes', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_item_detalhes_view_not_found_status_code(self):
        url = reverse_lazy('item_detalhes', kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_item_list_url_resolves_item_detalhes_view(self):
        view = resolve('/consulta_pn/item_detalhes/1/')
        self.assertEquals(view.func, item_detalhes)

    def test_item_list_view_contains_link_to_item_detalhes_page(self):
        item_detalhes_url = reverse_lazy('item_detalhes', kwargs={"pk": 1})
        self.assertContains(self.response, 'href="{0}"'.format(item_detalhes_url))


class ItemDetalhesTest(TestCase):
    def setUp(self):
        Item.objects.create(pn="A5053C", partName="ORING")
        url = reverse_lazy('consulta_pn')
        self.response = self.client.get(url)

    def test_item_detalhes_view_contains_link_back_to_homepage(self):
        item_detalhes_url = reverse_lazy('item_detalhes', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(item_detalhes_url))

    def test_item_detalhes_view_contains_link_back_to_consulta_pn(self):
        item_detalhes_url = reverse_lazy('item_detalhes', kwargs={'pk': 1})
        url = reverse_lazy('consulta_pn')
        self.assertContains(self.response, 'href="{0}'.format(url))

class CadastroPedidoTest(TestCase):
    def setUp(self):
        url = reverse_lazy('signup')
        data = {
            'username': 'john',
            'email': 'john@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.url = reverse_lazy('home')
        self.response = self.client.get(url)
        self.cadastro_pedido_url = reverse_lazy('cadastro_pedido')
        self.response = self.client.get(self.cadastro_pedido_url)

    def test_cadastro_pedido_view_contains_link_back_to_homepage(self):
        self.assertContains(self.response, 'href="{0}"'.format(self.url))

    def test_cadastro_pedido_form(self):
        form = NewOrderForm()
        expected = ['customer', 'received_date', 'fornecedor', 'date_sent_vendor',
                  'number', 'proforma', 'invoice', 'instrucoes', 'embarcado_finalizado_em',
                  'awb', 'tracking', 'moeda', 'amount_total', 'responsavel_fdb', 'tipo_embarque',
                  'termo_pagto', 'vencimento', 'pago', 'prioridade'
                  ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_cadastro_pedido_page_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_cadastro_pedido_url_resolves_cadastro_pedido_view(self):
        view = resolve('/cadastro_pedido/')
        self.assertEquals(view.func, cadastro_pedido)