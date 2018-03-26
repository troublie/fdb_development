from django.urls import resolve, reverse_lazy
from django.test import TestCase
from .views import cadastrar

class CadastrarTest(TestCase):
    def test_cadastrar_status_code(self):
        url = reverse_lazy('cadastrar')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_cadastrar_url_resolves_cadastrar_view(self):
        view = resolve('/cadastrar/')
        self.assertEquals(view.func, cadastrar)