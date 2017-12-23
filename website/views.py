from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Shelf, Load
from .forms import ShelfForm

def index(request):
    return HttpResponse("Hello world, you're at the website index.")

def shelves_list(request):
    shelves = Shelf.objects.all()
    loads = []
    for shelf in shelves:
        loads.append(shelf.load_set.all().order_by('load_type'))
    shelves_with_loads = zip(shelves, loads)
    return render(request, 'website/shelves_list.html', {'shelves_with_loads': shelves_with_loads})

def shelf_new(request):
    if request.method == 'POST':
        form = ShelfForm(request.POST)
        if form.is_valid():
            shelf = form.save()
            return redirect('shelves_list')
    else:   # TODO: editing shelves?
        form = ShelfForm()
    return render(request, 'website/shelf_edit.html', {'form': form})
