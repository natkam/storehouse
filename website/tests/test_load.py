import django
django.setup()

from django.test import TestCase
from ..models import Load, Transport, Shelf

class TestLoad(TestCase):
    def setUp(self):
        Load.objects.create(load_type='A', id=0)

    def test_load(self):
        unit0 = Load.objects.get(id=0)
        assert unit0.load_type == 'A'
        assert unit0.shelf == None
        assert unit0.transport == None

    def test_load_functions(self):
        unit0 = Load.objects.get(id=0)
        assert unit0.__str__() == 'id 0, Apples'
        # unit0.add_to_shelf_validator()
        # assert unit0.shelf.number == 7
        # shelf7 = Shelf.objects.get(number=7)
        # assert unit0.shelf == shelf7
        # unit0.transfer_validator()
        # assert unit0.shelf == None
        # assert unit0.transport == Transport.objects.get(number=1)
