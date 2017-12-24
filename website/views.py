from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Shelf, Transport, Load, Section
from .forms import ShelfForm, TransportForm

def index(request):
    return HttpResponse("Hello world, you're at the website index.")

# def shelves_list(request):
#     shelves = Shelf.objects.all()
#     loads = []
#     for shelf in shelves:
#         loads.append(shelf.load_set.all().order_by('load_type'))
#     shelves_with_loads = zip(shelves, loads)
#     return render(request, 'website/shelves.html', {'shelves_with_loads': shelves_with_loads})
#
# # TODO: DRY!!
# def transports_list(request):
#     transports = Transport.objects.all()
#     loads = []
#     for transport in transports:
#         loads.append(transport.load_set.all().order_by('load_type'))
#     transports_with_loads = zip(transports, loads)
#     return render(request, 'website/transports.html', {'transports_with_loads': transports_with_loads})
#
# def shelf_new(request):
#     if request.method == 'POST':
#         form = ShelfForm(request.POST)
#         if form.is_valid():
#             shelf = form.save()
#             return redirect('section_list', url_name='shelves')
#     else:   # TODO: editing shelves?
#         form = ShelfForm()
#     return render(request, 'website/shelf_edit.html', {'form': form})

def section_new(request, url_name):
    section = get_object_or_404(Section, url_name=url_name)
    model_forms = [ShelfForm, TransportForm]
    if url_name == 'shelves':
        model_form = model_forms[0]
    elif url_name == 'transports':
        model_form = model_forms[1]
    if request.method == 'POST':
        form = model_form(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('section_list', url_name=url_name)
    else:
        form = model_form()
    return render(
        request,
        'website/'+url_name+'_edit.html',
        {'section': section, 'form': form}
    )



def section_list(request, url_name):
    section = get_object_or_404(Section, url_name=url_name)
    loads = []
    if url_name == 'shelves':
        objs = Shelf.objects.all()
    elif url_name == 'transports':
        objs = Transport.objects.all()
    else:
        url_name = 'base'
        objs = []
    for obj in objs:
        loads.append(obj.load_set.all().order_by('load_type'))
    objs_with_loads = zip(objs, loads)
    return render(
        request,
        'website/'+url_name+'.html',
        {'section': section, 'objs_with_loads': objs_with_loads},
    )
