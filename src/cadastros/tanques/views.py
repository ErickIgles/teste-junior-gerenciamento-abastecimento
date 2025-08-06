from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.core.paginator import Paginator

from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Tanque
from .forms import TanqueForm



class TanqueCadastroView(CreateView):
    model = Tanque
    form_class = TanqueForm
    template_name = 'tanques/tanque_form.html'
    success_url = reverse_lazy('cadastros:tanques:listar')


class TanqueListarView(ListView):
    model = Tanque
    context_object_name = 'tanques'
    template_name = 'tanques/tanque_lista.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(tipo_combustivel__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)    
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_objetos = context.get('object_list')
        paginator = Paginator(lista_objetos, 2)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class TanqueAtualizarView(UpdateView):
    model = Tanque
    form_class = TanqueForm
    context_object_name = 'tanque'
    template_name = 'tanques/tanque_form.html'
    success_url = reverse_lazy('cadastros:tanques:listar')


class TanqueDeletarView(DeleteView):
    model = Tanque
    context_object_name = 'tanque'
    template_name = 'tanques/tanque_form_delete.html'
    success_url = reverse_lazy('cadastros:tanques:listar')