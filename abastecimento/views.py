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
    success_url = reverse_lazy('listagem_tanque')


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


class CriarBombaView(CreateView):
    model = Bomba
    form_class = BombaForm
    template_name = 'abastecimento/bomba_form.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context


class ListaBombaView(ListView):
    model = Bomba
    queryset = Bomba.objects.all()
    context_object_name = 'bombas'
    template_name = 'abastecimento/bomba_lista.html'


class AtualizarBombaView(UpdateView):
    model = Bomba
    form_class = BombaForm
    context_object_name = 'bomba'
    template_name = 'abastecimento/bomba_form.html'
    success_url = reverse_lazy('listagem_bomba')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context 


class DeletarBombaView(DeleteView):
    model = Bomba
    context_object_name = 'bomba'
    template_name = 'abastecimento/bomba_form_delete.html'
    success_url = reverse_lazy('listagem_bomba')


