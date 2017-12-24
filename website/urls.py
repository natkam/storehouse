from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<url_name>/', views.section_list, name='section_list'),
    path('<url_name>/new/', views.section_new, name='section_new'),
    # path('transports/', views.section_list, name='transports_list'),
    # path('transport/new/', views.shelf_new, name='transport_new'),
    # path('<url_name>/', views.section_detail, name='section_detail'),
]
