from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Shelf

def index(request):
    return HttpResponse("Hello world, you're at the website index.")

def shelves_list(request):
    shelves = Shelf.objects.all()
    return render(request, 'website/shelves_list.html', {'shelves': shelves})
