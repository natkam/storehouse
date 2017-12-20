from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Shelf, Load

def index(request):
    return HttpResponse("Hello world, you're at the website index.")

def shelves_list(request):
    shelves = Shelf.objects.all()
    loads = []
    for shelf in shelves:
        loads.append(shelf.load_set.all().order_by('load_type'))
    shelves_with_loads = zip(shelves, loads)
    # loads1 = shelves.get(number=1).load_set.all().order_by('load_type')
    return render(request, 'website/shelves_list.html', {'shelves': shelves, 'loads': loads, 'shelves_with_loads': shelves_with_loads})
#
