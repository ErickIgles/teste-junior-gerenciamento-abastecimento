from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import RegistroAbastecimento
from .forms import AbastecimentoForm
from cadastros.tanques.models import Tanque







class RegistroAbastecimentoCadastroView(CreateView):
    model = RegistroAbastecimento
    form_class = AbastecimentoForm
    template_name = 'abastecimento/abastecimento_form.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context


class RegitroAbastecimentoListaView(ListView):
    model = RegistroAbastecimento
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


class RegistroAbastecimentoAtualizarView(UpdateView):
    model = RegistroAbastecimento
    form_class = AbastecimentoForm
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/abastecimento_form_atualizar.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context


class RegistroAbastecimentoDeletarView(DeleteView):
    model = RegistroAbastecimento
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/abastecimento_form_delete.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')

