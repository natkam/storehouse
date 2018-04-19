"""
Sort the shelves in the storehouse during the night.

Transports of particular goods come in a given order, so the idea is to prepare
the storehouse during the night: put shelves with the zeroth type of load (at
least 5 loads, if they exist) in the beginning of the queue, then shelves with
the first type (>= 5 loads), etc. - so that the least possible number of shifts
is necessary during the day, while serving transports.

Warning: it has been assumed that there is max. 10 shelves, i.e. exactly the
same number as available positions. Additional shelves without the position
attribute set may lead to unexpected results.
"""

# TODO:
# After a given transport leaves, the last shelf from which it took loads stays at
# the beginnig of the line. Therefore it would be reasonable to take into account
# more than just one type of load on each shelf.
#
# The algorithm is 'greedy', i.e. it tries to maximise the number of loads of
# the given type at the shelves closest to the beginning of the line. It could
# be more effective to take into account also the following transports.


import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storehouse.settings")
django.setup()
# ^ tmp

from collections import Counter

from website.models import (
    Shelf, Transport, Load, MAX_LOADS_IN_TRANSPORT,
)
from transfer_loads import (
    get_transports_order, transfer_all,
)


def get_load_counts_on_one_shelf(shelf):
    """ Return a Counter (a dict subclass), e.g. {'A': 3, 'D': 7}. """
    loads_counter = Counter()
    load_types = shelf.load_set.values_list('load_type', flat=True)

    for type_letter in load_types:
        loads_counter[type_letter] += 1

    return loads_counter


def get_load_counts(shelves):
    """ Return a dict: key=shelf.number, value=get_load_counts_on_one_shelf() (a dict too). """
    loads = {}

    for shelf in shelves:
        loads[shelf.number] = get_load_counts_on_one_shelf(shelf)

    return loads


# TODO: those nested loops, and the if on top of that... Any way to refactor this?
def get_shelves_with_load_type(tr_load_type, all_shelves_with_load_counts):
    """ Return a list of tuples: (shelf_number, load_count). """
    shelves_with_the_load_type = []

    for shelf_number, shelf_loads in all_shelves_with_load_counts.items():
        for load_type, load_count in shelf_loads.items():
            if load_type == tr_load_type:
                shelves_with_the_load_type.append((shelf_number, load_count))

    return shelves_with_the_load_type


def sort_shelves_with_load_type(shelves_to_sort):
    """ Return a list of tuples: (shelf_number, load_count), sorted by descending load_count. """
    sorted_shelves = sorted(shelves_to_sort, key=lambda pair: pair[1], reverse=True)
    return sorted_shelves


# TODO: this function is quite big and complex. Would be nice to break it into smaller pieces.
def get_shelves_order():
    """ Return a list of shelves' numbers in order (list index == the right position). """
    transports_order = get_transports_order()
    all_shelves_with_load_counts = get_load_counts(all_shelves)   # dict
    sorted_shelves_list = []

    for tr_type in transports_order:
        shelves_to_sort = get_shelves_with_load_type(tr_type, all_shelves_with_load_counts)
        tmp_sorted_shelves = sort_shelves_with_load_type(shelves_to_sort) # list of tuples
        loads_in_transport = 0

        while tmp_sorted_shelves:
            shelf_with_highest_count = tmp_sorted_shelves.pop(0)
            sorted_shelves_list.append(shelf_with_highest_count)
            del shelves_to_sort[shelf_with_highest_count[0]]
            loads_in_transport += shelf_with_highest_count[1]

            if loads_in_transport >= MAX_LOADS_IN_TRANSPORT:
                break

    sorted_shelves_list = [shelf[0] for shelf in sorted_shelves_list]
    sorted_shelves_list += shelves_to_sort.keys()

    return sorted_shelves_list


def sort_shelves_in_db(all_shelves):
    for shelf in all_shelves:
        shelf.position = None
        shelf.save()

    sorted_shelves_list = get_shelves_order()
    position = 0

    for sorted_shelf_number in sorted_shelves_list:
        shelf_object = all_shelves.get(number=sorted_shelf_number)
        shelf_object.position = position
        shelf_object.save()
        position += 1


all_shelves = Shelf.objects.all().order_by('number')
# TODO: Find some consistent way of assuring that shelves without position set do not make the script fail.

sort_shelves_in_db(all_shelves)

shifts_counter = transfer_all()
