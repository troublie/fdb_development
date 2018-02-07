from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase
from .views import home, consulta_pn
from .models import Item


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse_lazy('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class ItemListTests(TestCase):
    def setUp(self):
        Item.objects.create(pn="A5053C", partName="ORING")

    def test_itemList_view_success_status_code(self):
        url = reverse_lazy('consulta_pn')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_itemList_url_resolves_itemList_view(self):
        view = resolve('/consulta_pn/')
        self.assertEquals(view.func, consulta_pn)
