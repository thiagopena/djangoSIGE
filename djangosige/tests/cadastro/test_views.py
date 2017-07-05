from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AdicionarClienteTestCase(TestCase):        
    def test_adicionar_cliente_resolves(self):
        self.url = reverse('cadastro:addclienteview')
        self.client = Client()
