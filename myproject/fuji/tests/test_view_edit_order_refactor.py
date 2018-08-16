from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse, resolve
from ..models import Order, Moeda, Prioridade, Tipo_emb, Fornecedor, Termo, Customer
from ..views import OrderUpdateView
from django.test import TestCase
from model_mommy import mommy


class OrderUpdateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
