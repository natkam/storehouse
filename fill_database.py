"""
Run:

python manage.py flush   # remove all data from the db
python fill_database.py

This script creates full set of Shelves and Transports, fills the shelves with
random loads, and handles transfering loads from shelves to transports appropriately.
"""

import django
django.setup()

from random import choice
from website.models import Shelf, Transport, Load
from website.models import LOAD_TYPES, MAX_TYPES_OF_LOAD_ON_SHELF, MAX_LOADS_ON_SHELF, MAX_NUMBER_OF_SHELVES, MAX_NUMBER_OF_TRANSPORTS

def create_shelves():
    for i in range(MAX_NUMBER_OF_SHELVES):
        new_shelf = Shelf.objects.create(number=i, position=i)
        new_shelf.save()

def create_random_transports():
    for i in range(MAX_NUMBER_OF_TRANSPORTS):
        transport = Transport.objects.create(number=i, load_type=choice(LOAD_TYPES))
        transport.save()

def generate_random_loads_for_one_shelf():
    types_of_load = []
    for i in range(MAX_TYPES_OF_LOAD_ON_SHELF):
        types_of_load.append(choice(LOAD_TYPES)[0])
    loads_pattern = []
    for i in range(MAX_LOADS_ON_SHELF):
        loads_pattern.append(choice(types_of_load))
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
