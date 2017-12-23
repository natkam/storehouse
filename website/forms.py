from django import forms

from .models import Shelf, Transport, Load

class ShelfForm(forms.ModelForm):

    class Meta:
        model = Shelf
        fields = ('number', 'position')

class TransportForm(forms.ModelForm):

    class Meta:
        model = Transport
        fields = ('number', 'load_type')

class LoadForm(forms.ModelForm):

    class Meta:
        model = Load
        fields = ('load_type', 'shelf', 'transport')
