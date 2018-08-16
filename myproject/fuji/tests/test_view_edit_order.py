from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse, resolve

from ..models import Order, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Customer
from ..views import OrderUpdateView
from django.test import TestCase


class OrderUpdateViewTestCase(TestCase):
    '''
    Base test case to be used in all `OrderUpdateView` view tests
    '''

    def setUp(self):
        self.username = 'Pedro'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        user = User.objects.first()
        moeda = Moeda.objects.create(simbolo="USD", descricao="DOLAR")
        moeda = Moeda.objects.first()
        prioridade = Prioridade.objects.create(tipo="Alta")
        prioridade = Prioridade.objects.first()
        tipo_emb = Tipo_emb.objects.create(descricao="Spareparts")
        tipo_emb = Tipo_emb.objects.first()
        fornecedor = Fornecedor.objects.create(nome="Sojitz", endreco="Teste", email_contato="teste@gmail.com",
                                               nome_contato="Joao")
        fornecedor = Fornecedor.objects.first()
        termo = Termo.objects.create(dias="30")
        termo = Termo.objects.first()
        customer = Customer.objects.create(nome="Jabil", endreco="Teste", email_contato="teste2@gmail.com",
                                           nome_contato="Joao")
        customer = Customer.objects.first()

        self.order = Order.objects.create(customer=customer, fornecedor=fornecedor, number='123', moeda=moeda,
                                          amount_total='1200', responsavel_fdb=user, tipo_embarque=tipo_emb,
                                          termo_pagto=termo, prioridade=prioridade, invoice='555')
        self.url = reverse('edit_order', kwargs={'order_pk': Order.objects.all().first().pk})


class LoginRequiredOrderUpdateViewTests(OrderUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedOrdertUpdateViewTests(OrderUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        '''
        A topic should be edited only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        '''
        self.assertEquals(self.response.status_code, 404)


class OrderUpdateViewTests(OrderUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/pedido_detalhes/1/edit/')
        self.assertEquals(view.func.view_class, OrderUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf + inputs + selects
        '''
        self.assertContains(self.response, '<input', 9)
        self.assertContains(self.response, '<select', 4)


class SuccessfulOrderUpdateViewTests(OrderUpdateViewTestCase):
    def setUp(self):
        super().setUp()

        url_edit = reverse('edit_order', kwargs={'order_pk': Order.objects.all().first().pk})
        user = User.objects.all().first()

        data = {
            'customer': "1", 'received_date': "27/01/2018", 'fornecedor': "1",
            'date_sent_vendor': "27/01/2018", 'number': "12345", 'proforma': "12345",
            'invoice': "12345", 'instrucoes': "DHL", 'embarcado_finalizado_em': "27/02/2018",
            'awb': "12345", 'tracking': "123456", 'moeda': "1", 'amount_total': "69000",
            'responsavel_fdb': "1", 'tipo_embarque': "1",
            'termo_pagto': "1", 'vencimento': "27/01/2019", 'pago': "1", 'prioridade': "1"
        }

        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(url_edit, data=data)
        self.order.refresh_from_db()

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        self.order.refresh_from_db()
        order_details_url = reverse('pedido_detalhes', kwargs={'pk': Order.objects.all().first().pk})
        self.assertRedirects(self.response, order_details_url)
        self.assertEqual(self.response.status_code, 302)

    def test_order_changed(self):
        self.order.refresh_from_db()
        self.assertEquals(self.order.amount_total, '69000')
