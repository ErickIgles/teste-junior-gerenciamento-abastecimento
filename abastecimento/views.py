from django.shortcuts import render


from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

from .models import Abastecimento, Tanque, Bomba
from .forms import AbastecimentoForm, TanqueForm, BombaForm


class IndexTemplateView(TemplateView):
    template_name = 'abastecimento/base.html'


class CriarTanqueView(CreateView):
    model = Tanque
    form_class = TanqueForm
    template_name = 'abastecimento/tanque_form.html'
    success_url = reverse_lazy('index')


class ListaTanqueView(ListView):
    model = Tanque
    queryset = Tanque.objects.all()
    context_object_name = 'tanques'
    template_name = 'abastecimento/tanque_lista.html'


class AtualizarTanqueView(UpdateView):
    model = Tanque
    form_class = TanqueForm
    context_object_name = 'tanque'
    template_name = 'abastecimento/tanque_form.html'
    success_url = reverse_lazy('listagem_tanque')


class DeletarTanqueView(DeleteView):
    model = Tanque
    context_object_name = 'tanque'
    template_name = 'abastecimento/tanque_form_delete.html'
    success_url = reverse_lazy('listagem_tanque')


