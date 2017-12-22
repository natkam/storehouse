import django
django.setup()

from django.test import TestCase
from ..models import Shelf

class TestShelf(TestCase):
    def setUp(self):
        Shelf.objects.create(number=0, position=4)

    def test_shelf(self):
        shelf0 = Shelf.objects.get(number=0)
        assert shelf0.position == 4

    def test_shelf_functions(self):
        shelf0 = Shelf.objects.get(number=0)
        assert shelf0.__str__() == '4: Shelf no. 0'
