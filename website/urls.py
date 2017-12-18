from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shelves/', views.shelves_list, name='shelves_list')
]
