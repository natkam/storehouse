"""
Create a full set of shelves and transports, and fill the shelves with random loads.

Run (bash console):
$ bash ./scripts/flush_and_fill.sh
to flush all the data from the DB and create a new set of objects (+ an admin account).
To set execute permissions:
$ chmod +x ./scripts/flush_and_fill.sh
"""

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storehouse.settings")
django.setup()

from random import choice
from website.models import (
    Shelf, Transport, Load,
    LOAD_TYPES, MAX_NUMBER_OF_SHELVES_IN_LINE, MAX_TYPES_OF_LOAD_ON_SHELF,
    MAX_LOADS_ON_SHELF, MAX_LOADS_IN_TRANSPORT, MAX_NUMBER_OF_TRANSPORTS,
)

def create_shelves():
    for i in range(MAX_NUMBER_OF_SHELVES_IN_LINE):
        new_shelf = Shelf.objects.create(number=i, position=i)
        new_shelf.save()


def create_random_transports():
    for i in range(MAX_NUMBER_OF_TRANSPORTS):
        transport = Transport.objects.create(number=i, load_type=choice(LOAD_TYPES)[0])
        transport.save()


def generate_random_loads_for_one_shelf():
    types_of_load = [choice(LOAD_TYPES)[0] for i in range(MAX_TYPES_OF_LOAD_ON_SHELF)]
    loads_pattern = [choice(types_of_load) for i in range(MAX_LOADS_ON_SHELF)]
    return loads_pattern


def fill_one_shelf_randomly(shelf):
    loads_pattern = generate_random_loads_for_one_shelf()
    for load_type in loads_pattern:
        new_load = Load.objects.create(load_type=load_type, shelf=shelf)
        new_load.save()


def fill_all_shelves():
    shelves = Shelf.objects.all()
    for shelf in shelves:
        fill_one_shelf_randomly(shelf)


create_shelves()
fill_all_shelves()
create_random_transports()
