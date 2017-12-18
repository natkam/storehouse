import django
django.setup()

import functools
from ..models import Transport

class TestTransport:
    def test_transport_decorator(func):
        @functools.wraps(func)
        def test_transport_with_data(self):
            trans0 = Transport.objects.create(number=0)
            func(self)
            Transport.objects.get(number=0).delete()
        return test_transport_with_data

    @test_transport_decorator
    def test_transport(self):
        trans0 = Transport.objects.get(number=0)
        assert trans0.number == 0
        assert trans0.product_type == 'A'
        assert trans0.load_size == 0

    @test_transport_decorator
    def test_transport_functions(self):
        trans0 = Transport.objects.get(number=0)
        trans0.fill()
        assert trans0.load_size == 5
