# tmp!!!
import django
django.setup()
# ^ tmp!!!

from website.models import *
from transfer_loads import get_transports_order, shift_shelves, transfer_loads_to_one_transport

ALL_SHELVES = Shelf.objects.all().order_by('number')

def get_load_counts_on_one_shelf(shelf):
    shelf_types = shelf.load_set.values_list('load_type', flat=True).order_by('load_type')
    shelf_types_list = list(shelf_types)
    distinct_shelf_types = set(shelf_types_list)
    load_counts = {}
    for load_type in distinct_shelf_types:
        count = shelf_types_list.count(load_type)  # shelf_types - a QuerySet, not a list!
        load_counts[load_type] = count
    return load_counts

def get_load_counts_on_all_shelves():
    all_loads = {}
    for shelf in ALL_SHELVES:
        one_shelf_loads = get_load_counts_on_one_shelf(shelf)
        all_loads[shelf.number] = one_shelf_loads
    return all_loads

def sort_shelves_with_given_load(tr_load_type, shelves_to_sort):
    # print(shelves_to_sort)
    sorted_shelves = []
    for shelf in shelves_to_sort:
        for load_type in shelves_to_sort[shelf]:
            if load_type == tr_load_type:
                sorted_shelves.append((shelf, shelves_to_sort[shelf][load_type]))
    sorted_shelves.sort(key=lambda pair: pair[1], reverse=True)
    print('function', sorted_shelves)
    return sorted_shelves

transports_order = get_transports_order()
shelves_to_sort = get_load_counts_on_all_shelves()   # dict
sorted_shelves_list = []
# for transport_type in transports_order:
for tr_type in transports_order:
    print('tr_type', tr_type)
    tmp_sorted_shelves = sort_shelves_with_given_load(tr_type, shelves_to_sort) # list of tuples
    if not tmp_sorted_shelves:
        continue
    loads_in_transport = 0
    i = 0
    sorted_shelves_list.append(tmp_sorted_shelves.pop(0))
    print(sorted_shelves_list, sorted_shelves_list[-1][0])
    del shelves_to_sort[sorted_shelves_list[-1][0]]
    loads_in_transport += sorted_shelves_list[-1][1]
    if tmp_sorted_shelves[0][1] >= MAX_LOADS_IN_TRANSPORT:
        loads_in_transport = MAX_LOADS_IN_TRANSPORT
        # return # break?
    else:
        while loads_in_transport < MAX_LOADS_IN_TRANSPORT and i < len(tmp_sorted_shelves):
            sorted_shelves_list.append(tmp_sorted_shelves.pop(i))
            print('while', sorted_shelves_list, sorted_shelves_list[-1][0])
            del shelves_to_sort[sorted_shelves_list[-1][0]]
            loads_in_transport += sorted_shelves_list[-1][1]
            i += 1
    print('last line', shelves_to_sort, loads_in_transport)
for shelf in shelves_to_sort:
    sorted_shelves_list.append((shelf, 0))
print('sorted_shelves_list:', sorted_shelves_list)
