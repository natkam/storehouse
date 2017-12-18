import django
django.setup()

import functools
from ..models import Shelf

class TestShelf():
    def test_shelf_decorator(func):
        @functools.wraps(func)
        def shelf_test_with_data(self):
            Shelf.objects.create(number=0, position=4)
            shelf0 = Shelf.objects.get(number=0)
            shelf0.prod1_type = 'A'
            shelf0.prod1_count = 5
            shelf0.prod2_type = 'B'
            shelf0.prod2_count = 1
            shelf0.prod3_type = 'C'
            shelf0.prod3_count = 6
            shelf0.save()
            func(self)
            shelf0.delete()
        return shelf_test_with_data

    # shelf0 = Shelf.objects.create(number=0, position=4)
    @test_shelf_decorator
    def test_shelf(self):
        shelf0 = Shelf.objects.get(number=0)
        assert shelf0.position == 4
        assert shelf0.prod1_count == 5
        assert shelf0.prod1_type == 'A'

    @test_shelf_decorator
    def test_shelf_functions(self):
        shelf0 = Shelf.objects.get(number=0)
        assert shelf0.__str__() == '4: Shelf no. 0'
        # assert shelf0.fill() == {'A': 5, 'B': 1, 'C': 6}
        shelf0.empty()
        assert shelf0.prod1_type == ''
        assert shelf0.prod1_count == 0
