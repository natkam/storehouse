# tmp!!!
import django
django.setup()
# ^ tmp!!!
# from website.models import Shelf, Load, Transport
# from website.models import LOAD_TYPES, MAX_TYPES_OF_LOAD_ON_SHELF, MAX_LOADS_ON_SHELF, MAX_NUMBER_OF_SHELVES, MAX_NUMBER_OF_TRANSPORTS
from website.models import *

def get_transports_order():
    transports_order = []
    transports_types = Transport.objects.values_list('load_type', flat=True).order_by('number')
    # transport_types is a QuerySet - a list of strings: 'A', 'B', etc.
    for type_letter in transports_types:
        transports_order.append(type_letter)
    return transports_order

def transfer_one_load(load, transport):
    load.shelf = None
    load.transport = transport
    load.save()

def transfer_loads_from_shelf(shelf, transport):
    loads_on_shelf = shelf.load_set.all()
    transport_type_letter = transport.load_type
    load_counter = transport.load_set.count()
    for load in loads_on_shelf:
        if load.load_type == transport_type_letter:
            transfer_one_load(load, transport)
            load_counter += 1
            if load_counter >= MAX_LOADS_IN_TRANSPORT:
                break
    return load_counter

def shift_shelves(last_shelf_position):
    """ 'last_shelf_position' is the position of the shelf which stays in the front of the line. """
    shelves = Shelf.objects.all()  # .order_by('position')
    aside = []
    for shelf in shelves:
        if shelf.position < last_shelf_position:
            aside.append(shelf)
            shelf.position = None
        else:
            shelf.position -= last_shelf_position
        shelf.save()  # is it necessary already? think so!
    for old_position in range(last_shelf_position):
        shelf = aside[old_position]
        shelf.position = MAX_NUMBER_OF_SHELVES + old_position - last_shelf_position
        shelf.save()

def transfer_loads_to_one_transport(transport):
    load_counter = transport.load_set.count()
    last_shelf_position = 0
    shelves = Shelf.objects.all()
    for shelf in shelves:
        load_counter = transfer_loads_from_shelf(shelf, transport)
        print(shelf.number, load_counter)
        if load_counter >= MAX_LOADS_IN_TRANSPORT:
            last_shelf_position = shelf.position
            break
    if last_shelf_position:
        shift_shelves(last_shelf_position)

tr = Transport.objects.get(number=3)
if tr.load_set.count() < MAX_LOADS_IN_TRANSPORT:
    transfer_loads_to_one_transport(tr)
