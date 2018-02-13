from django.urls import reverse_lazy
from django.urls import resolve
from django.test import TestCase
from .views import home, consulta_pn, item_detalhes
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
