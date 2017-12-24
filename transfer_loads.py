"""
Handle transfering loads from shelves to transports appropriately.
"""

import django
django.setup()

from website.models import (
    Shelf, Transport, Load,
    LOAD_TYPES, MAX_NUMBER_OF_SHELVES_IN_LINE, MAX_TYPES_OF_LOAD_ON_SHELF,
    MAX_LOADS_ON_SHELF, MAX_LOADS_IN_TRANSPORT, MAX_NUMBER_OF_TRANSPORTS,
)


def get_transports_order():
    transports_types = Transport.objects.values_list('load_type', flat=True).order_by('number')
    # transport_types is a QuerySet, e.g. <QuerySet ['B', 'E', 'A', 'A', 'B']>
    transports_order = list(transports_types)
    return transports_order


def transfer_one_load(load, transport):
    load.shelf = None
    load.transport = transport
    load.save()


def transfer_loads_from_one_shelf(shelf, transport):
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
    """ Arg is the position of the shelf which stays in the front of the queue. """
    shelves = Shelf.objects.filter(position__isnull=False)  # .order_by('position')
    aside = []
    for shelf in shelves:
        if shelf.position < last_shelf_position:
            aside.append(shelf)
            shelf.position = None
        else:
            shelf.position -= last_shelf_position
        shelf.save()
    for old_position in range(last_shelf_position):
        shelf = aside[old_position]
        shelf.position = MAX_NUMBER_OF_SHELVES_IN_LINE + old_position - last_shelf_position
        shelf.save()


def transfer_loads_to_one_transport(transport):
    load_counter = transport.load_set.count()
    last_shelf_position = 0
    shelves = Shelf.objects.filter(position__isnull=False)
    for shelf in shelves:
        load_counter = transfer_loads_from_one_shelf(shelf, transport)
        if load_counter >= MAX_LOADS_IN_TRANSPORT:
            last_shelf_position = shelf.position
            break
    if last_shelf_position:
        shift_shelves(last_shelf_position)
    return last_shelf_position


def transfer_all():
    all_transports = Transport.objects.all()
    shifts_counter = 0
    for tr in all_transports:
        if tr.load_set.count() < MAX_LOADS_IN_TRANSPORT:
            shifts_counter += transfer_loads_to_one_transport(tr)
    return shifts_counter


# shifts_counter = transfer_all()
# print('Shelf shifts performed:', shifts_counter)
