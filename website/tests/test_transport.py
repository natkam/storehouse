import django
django.setup()

import functools
from django.test import TestCase
from ..models import Transport

class TestTransport(TestCase):
    def setUp(self):
        Transport.objects.create(number=0)

    def test_transport(self):
        trans0 = Transport.objects.get(number=0)
        assert trans0.number == 0
        assert trans0.load_type == 'A'

    def test_transport_functions(self):
        trans0 = Transport.objects.get(number=0)
        assert trans0.__str__() == 'Transport no. 0, Apples'
