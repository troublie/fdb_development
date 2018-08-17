from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse, resolve
from ..models import Order, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Customer
from ..views import OrderUpdateView
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key


class OrderUpdateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = mommy.make('User',
                              username='Pedro',
                              is_active=True)
        cls.user.set_password('password')
        cls.user.save()
        cls.order = mommy.make(Order, responsavel_fdb=cls.user)
        print("Order criada por %s" % cls.order.responsavel_fdb)
        print("O pk da order é %s" % cls.order.pk)
        print("O username é %s" % cls.user.username)
        print("O pass é %s" % cls.user.password)

    def setUp(self):
        self.url = reverse('edit_order', kwargs={'order_pk': Order.objects.all().first().pk})

    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

    def test_unauthorized_ordert_update_view(self):
        username = 'jane'
        password = '321'
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_order_update_view(self):
        self.client.login(username='Pedro', password='password')
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/pedido_detalhes/1/edit/')
        self.assertEquals(view.func.view_class, OrderUpdateView)

    def test_csrf(self):
        self.response = self.client.get(self.url)
        print (self.response.content)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        self.response = self.client.get(self.url)
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf + inputs + selects
        '''
        self.response = self.client.get(self.url)
        self.assertContains(self.response, '<input', 9)
        self.assertContains(self.response, '<select', 4)
