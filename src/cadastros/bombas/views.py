from django.shortcuts import render

from django.core.paginator import Paginator

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Bomba
from .forms import BombaForm


from ..tanques.models import Tanque


class BombaCadastroView(CreateView):
    model = Bomba
    form_class = BombaForm
    template_name = 'bombas/bomba_form.html'
    success_url = reverse_lazy('cadastros:bombas:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context


class BombaListarView(ListView):
    model = Bomba
    context_object_name = 'bombas'
    template_name = 'bombas/bomba_lista.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(nome_bomba__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_objetos = context.get('object_list')
        pagination = Paginator(lista_objetos, 2)
        
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class BombaAtualizarView(UpdateView):
    model = Bomba
    form_class = BombaForm
    context_object_name = 'bomba'
    template_name = 'bombas/bomba_form_atualizar.html'
    success_url = reverse_lazy('cadastros:bombas:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context 


class BombaDeletarView(DeleteView):
    model = Bomba
    context_object_name = 'bomba'
    template_name = 'bombas/bomba_form_delete.html'
    success_url = reverse_lazy('cadastros:bombas:listar')

