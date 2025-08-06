from django import forms
from .models import Bomba





class BombaForm(forms.ModelForm):

    class Meta:
        model = Bomba
        fields = ['nome_bomba', 'tanque']

