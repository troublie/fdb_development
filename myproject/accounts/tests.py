from django.urls import resolve, reverse_lazy
from django.test import TestCase
from .views import signup

class SignUpTest(TestCase):
    def test_signup_status_code(self):
        url = reverse_lazy('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)