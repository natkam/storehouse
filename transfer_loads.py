"""
Handle transfering loads from shelves to transports appropriately.
"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storehouse.settings")
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


def put_shelf_aside(shelf, aside):
    aside.append(shelf)
    shelf.position = None
    shelf.save()

def move_shelf_to_front(shelf, shift):
    shelf.position -= shift
    shelf.save()

def put_shelf_from_aside_back(shelf, aside, shift):
    old_position = aside.index(shelf)
    shelf.position = MAX_NUMBER_OF_SHELVES_IN_LINE + old_position - shift
    shelf.save()


def shift_shelves(shift):
    """ shift == current position of the shelf which will end up in the front of the queue. """
    shelves = Shelf.objects.filter(position__isnull=False)  # .order_by('position')
    aside = []

    for shelf in shelves:
        if shelf.position < shift:
            put_shelf_aside(shelf, aside)
        else:
            move_shelf_to_front(shelf, shift)

    for shelf in aside:
        put_shelf_from_aside_back(shelf, aside, shift)


def transfer_loads_to_one_transport(transport):
    load_counter = transport.load_set.count()
    shift = 0
    shelves = Shelf.objects.filter(position__isnull=False)

    for shelf in shelves:
        load_counter = transfer_loads_from_one_shelf(shelf, transport)

        if load_counter >= MAX_LOADS_IN_TRANSPORT:
            shift = shelf.position
            break

    if shift:
        shift_shelves(shift)

    return shift


def transfer_all():
    all_transports = Transport.objects.all()
    shifts_counter = 0

    for tr in all_transports:
        if tr.load_set.count() < MAX_LOADS_IN_TRANSPORT:
            shifts_counter += transfer_loads_to_one_transport(tr)

    return shifts_counter


# TODO: define a class perhaps, instead of passing arguments that are changed and returned?
