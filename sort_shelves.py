# tmp!!!
import django
django.setup()
# ^ tmp!!!
# from website.models import Shelf, Load, Transport
# from website.models import LOAD_TYPES, MAX_TYPES_OF_LOAD_ON_SHELF, MAX_LOADS_ON_SHELF, MAX_NUMBER_OF_SHELVES, MAX_NUMBER_OF_TRANSPORTS
from website.models import *

def get_load_type_letter(load_type):
    # load_type is in the form "('A', 'Apples')"
    return load_type[2]
# Yeah, this is ugly... Use some smart string methods perhaps?

def get_transports_order():
    transports_order = []
    transports_types = Transport.objects.values_list('load_type', flat=True).order_by('number')
    # transport_types is a QuerySet - a list of strings in the form "('A', 'Apples')"
    for types_string in transports_types:
        type_letter = get_load_type_letter(types_string)
        transports_order.append(type_letter)
    return transports_order

def transfer_one_load(load, transport):
    load.shelf = None
    load.transport = transport
    load.save()

def transfer_loads_from_shelf(shelf, transport):
    loads_on_shelf = shelf.load_set.all()
    transport_type_letter = get_load_type_letter(transport.load_type)
    transport_load_counter = transport.load_set.count()
    for load in loads_on_shelf:
        if load.load_type == transport_type_letter:
            transfer_one_load(load, transport)
            transport_load_counter += 1
            if transport_load_counter >= MAX_LOADS_IN_TRANSPORT:
                break
    return transport_load_counter

tr = Transport.objects.get(number=0)
shelves = Shelf.objects.all().order_by('position')

counter = tr.load_set.count()
if counter < MAX_LOADS_IN_TRANSPORT:
    for shelf in shelves:
        counter = transfer_loads_from_shelf(shelf, tr)
        print(shelf.number, counter)
        if counter >= MAX_LOADS_IN_TRANSPORT:
            break
