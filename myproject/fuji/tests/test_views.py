from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.urls import resolve
from django.test import TestCase

from ..forms import NewOrderForm
from ..views import home, consulta_pn, item_detalhes, cadastro_pedido, lista_pedido
from ..models import Item, Customer, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Order


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


class CadastroPedidoViewTest(TestCase):
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

    def test_cadastro_pedido_form(self):
        form = NewOrderForm()
        expected = ['customer', 'received_date', 'fornecedor', 'date_sent_vendor',
                    'number', 'proforma', 'invoice', 'instrucoes', 'embarcado_finalizado_em',
                    'awb', 'tracking', 'moeda', 'amount_total', 'responsavel_fdb', 'tipo_embarque',
                    'termo_pagto', 'vencimento', 'pago', 'prioridade'
                    ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class CadatroPedidoTest(TestCase):
    def setUp(self):
        url = reverse_lazy('cadastro_pedido')
        self.response = self.client.get(url)

    def test_cadastro_pedido_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_cadastro_pedido_url_resolves_cadastro_pedido_view(self):
        view = resolve('/cadastro_pedido/')
        self.assertEquals(view.func, cadastro_pedido)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewOrderForm)

    def test_form_inputs(self):
        self.assertContains(self.response, 'form-group', 19)

    def test_cadastro_pedido_view_contains_link_back_to_homepage(self):
        url = reverse_lazy('home')
        self.assertContains(self.response, 'href="{0}"'.format(url))


class CadastroPedidoSucesso(TestCase):
    def setUp(self):
        self.moeda = Moeda.objects.create(simbolo="USD", descricao="DOLAR")
        self.prioridade = Prioridade.objects.create(tipo="Alta")
        self.tipo_emb = Tipo_emb.objects.create(descricao="Spare parts")
        self.fornecedor = Fornecedor.objects.create(nome="Jabil", endreco="Teste", email_contato="teste@gmail.com",
                                                    nome_contato="Joao")
        self.termo = Termo.objects.create(dias="30")
        self.customer = Customer.objects.create(nome="Sojitz", endreco="Teste", email_contato="teste2@gmail.com",
                                                nome_contato="Joao")
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')

    def test_cadastro_sucesso(self):
        data = {
            'customer': "1", 'received_date': "27/01/2018", 'fornecedor': "1",
            'date_sent_vendor': "27/01/2018", 'number': "12345", 'proforma': "12345",
            'invoice': "12345", 'instrucoes': "DHL", 'embarcado_finalizado_em': "27/02/2018",
            'awb': "12345", 'tracking': "123456", 'moeda': "1", 'amount_total': "1200",
            'responsavel_fdb': "1", 'tipo_embarque': "1",
            'termo_pagto': "1", 'vencimento': "27/01/2019", 'pago': "1", 'prioridade': "1"
        }

        url = reverse_lazy('cadastro_pedido')
        homeUrl = reverse_lazy('home')
        response = self.client.post(url, data)
        self.assertRedirects(response, homeUrl)

    def test_cadastro_insucesso(self):
        data = {
            'customer': "5", 'received_date': "27/01/2018", 'fornecedor': "1",
            'date_sent_vendor': "27/01/2018", 'number': "12345", 'proforma': "12345",
            'invoice': "12345", 'instrucoes': "DHL", 'embarcado_finalizado_em': "27/02/2018",
            'awb': "12345", 'tracking': "123456", 'moeda': "1", 'amount_total': "1200",
            'responsavel_fdb': "5", 'tipo_embarque': "1",
            'termo_pagto': "1", 'vencimento': "27/01/2019", 'pago': "1", 'prioridade': "1"
        }

        url = reverse_lazy('cadastro_pedido')
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'form-group', 19)


class PedidoListViewTest(TestCase):
    def setUp(self):
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
