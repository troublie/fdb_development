from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase

from ..forms import NewOrderForm
from ..views import cadastro_pedido
from ..models import Customer, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo


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
        url = reverse_lazy('signup')
        data = {
            'username': 'john2',
            'email': 'john@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.url = reverse_lazy('home')
        self.response = self.client.get(url)
        self.cadastro_pedido_url = reverse_lazy('cadastro_pedido')
        self.response = self.client.get(self.cadastro_pedido_url)
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

class LoginRequiredFailCadastroPedido(TestCase):
    def setUp(self):
        self.url = reverse_lazy('cadastro_pedido')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse_lazy('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))