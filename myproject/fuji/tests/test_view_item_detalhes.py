from django.urls import reverse_lazy
from django.test import TestCase
from ..models import Item


class ItemDetalhesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(pn="A5053C", partname="ORING")
        cls.item = Item.objects.first()

    def setUp(self):
        url = reverse_lazy('consulta_pn')
        self.response = self.client.get(url)

    def test_item_detalhes_view_contains_link_back_to_homepage(self):
        item_detalhes_url = reverse_lazy('item_detalhes', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(item_detalhes_url))

    def test_item_detalhes_view_contains_link_back_to_consulta_pn(self):
        item_detalhes_url = reverse_lazy('item_detalhes', kwargs={'pk': 1})
        url = reverse_lazy('consulta_pn')
        self.assertContains(self.response, 'href="{0}'.format(url))
