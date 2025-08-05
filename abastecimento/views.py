from django.shortcuts import render

from django.core.paginator import Paginator
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
    context_object_name = 'tanques'
    template_name = 'abastecimento/tanque_lista.html'

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
    context_object_name = 'bombas'
    template_name = 'abastecimento/bomba_lista.html'


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
        pagination = Paginator(lista_objetos, 1)
        
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['page_obj'] = page_obj
        return context

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


class CriarRegistroAbastecimentoView(CreateView):
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'abastecimento/abastecimento_form.html'
    success_url = reverse_lazy('listagem_abastecimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bombas'] = Bomba.objects.all()
        return context

class ListaRegitroAbastecimentoView(ListView):
    model = Abastecimento
    context_object_name = 'abastecimentos'
    template_name = 'abastecimento/abastecimento_lista.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')


        if q:
            queryset = queryset.filter(bomba__nome_bomba__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_objetos = context.get('object_list')
        
        pagination = Paginator(lista_objetos, 1)

        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['page_obj'] = page_obj
        return context



class AtualizarRegistroAbastecimentoView(UpdateView):
    model = Abastecimento
    form_class = AbastecimentoForm
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/abastecimento_form.html'
    success_url = reverse_lazy('listagem_abastecimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bombas'] = Bomba.objects.all()
        return context
    
class DeletaRegistroAbastecimentoView(DeleteView):
    model = Abastecimento
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/abastecimento_form_delete.html'
    success_url = reverse_lazy('listagem_abastecimento')

