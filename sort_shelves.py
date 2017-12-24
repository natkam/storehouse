"""
Sort the shelves in the storehouse during the night.

Transport of particular goods come in a given order, so the idea is to prepare
the storehouse during the night: put shelves with the zeroth type of load (at
least 5 loads, if they exist) in the beginnig of the queue, then shelves with
the first type (>= 5 loads), etc. - so that the least possible number of shifts
is necessary during the day, while serving transports.
"""

# TODO:
# After a given transport leaves, the last shelf from which it took loads stays at
# the beginnig of the line. Therefore it would be reasonable to take into account
# more than just one type of load on each shelf.
#
# The algorithm is 'greedy', i.e. it tries to maximise the number of loads of
# the given type at the shelves closest to the beginning of the line. It could
# be more effective to take into account also the following transports.

# tmp!!!
import django
django.setup()
# ^ tmp!!!

from collections import Counter

from website.models import (
    Shelf, Transport, Load,
    LOAD_TYPES, MAX_NUMBER_OF_SHELVES, MAX_TYPES_OF_LOAD_ON_SHELF,
    MAX_LOADS_ON_SHELF, MAX_LOADS_IN_TRANSPORT, MAX_NUMBER_OF_TRANSPORTS,
)
from transfer_loads import (
    get_transports_order, shift_shelves, transfer_loads_to_one_transport,
)

all_shelves = Shelf.objects.all().order_by('number')


def get_load_counts_on_one_shelf(shelf):
    """ Return a Counter (a dict subclass), e.g. {'A': 3, 'D': 7}. """
    loads_counter = Counter()
    load_types = shelf.load_set.values_list('load_type', flat=True)
    for type_letter in load_types:
        loads_counter[type_letter] += 1
    return loads_counter


def get_load_counts_on_all_shelves():
    """ Return a dict: key=shelf.number, value=get_load_counts_on_one_shelf() (a dict too). """
    all_loads = {}
    for shelf in all_shelves:
        one_shelf_loads = get_load_counts_on_one_shelf(shelf)
        all_loads[shelf.number] = one_shelf_loads
    return all_loads


def sort_shelves_with_given_load(tr_load_type, shelves_to_sort):
    """ Return a sorted list of 'get_load_counts_on_one_shelf'-type-dicts. """
    sorted_shelves = []
    for shelf_number in shelves_to_sort:
        shelf_loads = shelves_to_sort[shelf_number]
        for load_type in shelf_loads:
            if load_type == tr_load_type:
                load_count = shelf_loads[load_type]
                sorted_shelves.append((shelf_number, load_count))
    sorted_shelves.sort(key=lambda pair: pair[1], reverse=True)
    return sorted_shelves


def get_shelves_order():
    """ Return a list of shelves' numbers in order (list index == the right position). """
    transports_order = get_transports_order()
    shelves_to_sort = get_load_counts_on_all_shelves()   # dict
    sorted_shelves_list = []
    for tr_type in transports_order:
        # print('tr_type', tr_type)
        tmp_sorted_shelves = sort_shelves_with_given_load(tr_type, shelves_to_sort) # list of tuples
        loads_in_transport = 0
        while tmp_sorted_shelves:
            shelf_with_highest_count = tmp_sorted_shelves.pop(0)
            sorted_shelves_list.append(shelf_with_highest_count)
            # print('while', sorted_shelves_list, shelf_with_highest_count[0])
            del shelves_to_sort[shelf_with_highest_count[0]]
            loads_in_transport += shelf_with_highest_count[1]
            if loads_in_transport >= MAX_LOADS_IN_TRANSPORT:
                break
        # print('last line', shelves_to_sort, loads_in_transport)
    sorted_shelves_list = [shelf[0] for shelf in sorted_shelves_list]
    sorted_shelves_list += shelves_to_sort.keys()
    # print('sorted_shelves_list:', sorted_shelves_list)
    return sorted_shelves_list


def sort_shelves_in_db():
    sorted_shelves_list = get_shelves_order()
    for shelf in all_shelves:
        shelf.position = None
        shelf.save()
    position = 0
    for sorted_shelf_number in sorted_shelves_list:
        shelf_object = all_shelves.get(number=sorted_shelf_number)
        shelf_object.position = position
        shelf_object.save()
        position += 1

sort_shelves_in_db()
