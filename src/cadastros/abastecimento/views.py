from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from .models import RegistroAbastecimento
from .forms import AbastecimentoForm
from cadastros.tanques.models import Tanque
from cadastros.funcionarios.models import Funcionario







class RegistroAbastecimentoCadastroView(LoginRequiredMixin, CreateView):
    model = RegistroAbastecimento
    form_class = AbastecimentoForm
    template_name = 'abastecimento/abastecimento_form.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')


    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = [grupo.name for grupo in Group.objects.all()]
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

    def get_initial(self):
        initial = super().get_initial()
        initial['funcionario'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.funcionario = self.request.user
        return super().form_valid(form)


class RegitroAbastecimentoListaView(LoginRequiredMixin, ListView):
    model = RegistroAbastecimento
    context_object_name = 'abastecimentos'
    template_name = 'abastecimento/abastecimento_lista.html'

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = [grupo.name for grupo in Group.objects.all()]
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

    def get_queryset(self):

        queryset = super().get_queryset()
        usuario = self.request.user

        if not usuario.is_staff:
            queryset = queryset.filter(funcionario=self.request.user)
        
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


class RegistroAbastecimentoAtualizarView(LoginRequiredMixin, UpdateView):
    model = RegistroAbastecimento
    form_class = AbastecimentoForm
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/abastecimento_form_atualizar.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = [grupo.name for grupo in Group.objects.all()]
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanques'] = Tanque.objects.all()
        return context


class RegistroAbastecimentoDeletarView(LoginRequiredMixin, DeleteView):
    model = RegistroAbastecimento
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/abastecimento_form_delete.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')


    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = [grupo.name for grupo in Group.objects.all()]
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

