from django.shortcuts import render


from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from .models import Abastecimento, Tanque
from .forms import AbastecimentoForm, TanqueForm


class IndexTemplateView(TemplateView):
    template_name = 'abastecimento/base.html'

