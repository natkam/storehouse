import django
django.setup()

from django.test import TestCase

from random import choice, randint, seed
from website.models import Shelf, Load, Transport
from sort_shelves import

class TestSortShelves(TestCase):
    fixtures = ['full_random']

    # def test_
