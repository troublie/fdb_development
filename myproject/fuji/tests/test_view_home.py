from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase
from ..views import home


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
