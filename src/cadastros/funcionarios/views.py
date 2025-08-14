from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioUpdateForm
from django.contrib.auth.models import Group



class FuncionarioCadastrarView(LoginRequiredMixin, CreateView):
    template_name = 'funcionarios/form_register.html'
    model = Funcionario
    form_class = FuncionarioForm
    success_url = reverse_lazy('home:index')

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if not usuario.is_authenticated:
            return redirect('home:index')

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = Group.objects.exclude(name='funcionarios')
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

    def form_valid(self, form):
        messages.success(self.request, f'Funcionário(a) {form.instance.nome_funcionario} cadastrado(a) com sucesso.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao realizar o cadastro. Confira as informações fornecidas.')
        return super().form_invalid(form)


class FuncionarioListarView(LoginRequiredMixin, ListView):
    template_name = 'funcionarios/lista_funcionario.html'
    model = Funcionario
    context_object_name = 'funcionarios'

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if not usuario.is_authenticated:
            return redirect('home:index')

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = Group.objects.exclude(name='funcionarios')
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(nome_funcionario__icontains=q)
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
    

class FuncionarioAtualizarView(LoginRequiredMixin, UpdateView):
    template_name = 'funcionarios/form_update.html'
    model = Funcionario
    context_object_name = 'funcionario'
    form_class = FuncionarioUpdateForm
    success_url = reverse_lazy('cadastros:funcionarios:listar')

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if not usuario.is_authenticated:
            return redirect('home:index')

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = Group.objects.exclude(name='funcionarios')
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')


    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.object.user.email
        return initial

    def form_valid(self, form):
        messages.success(self.request, f'Dados do(a) funcionário(a) {form.instance.nome_funcionario} atualizado com sucesso.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f'Erro ao tentar atualizar os dados. Confira as informações.')
        return super().form_invalid(form)

class FuncionarioDeletarView(LoginRequiredMixin, DeleteView):
    template_name = 'funcionarios/form_delete.html'
    model = Funcionario
    success_url = reverse_lazy('cadastros:funcionarios:listar')

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

        if not usuario.is_authenticated:
            return redirect('home:index')

        if usuario.is_staff:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            funcionario = Funcionario.objects.get(user=usuario)

            grupos = Group.objects.exclude(name='funcionarios')
            
            if funcionario.grupo and funcionario.grupo.name in grupos:
                return super().dispatch(request, *args, **kwargs)
            return redirect('home:index')
        except Funcionario.DoesNotExist:
            return redirect('home:index')

    def delete(self, request, *args, **kwargs):
        funcionario = self.get_object()
        nome_funcionario = funcionario.nome_funcionario
        messages.success(request, f'Funcionário(a) {nome_funcionario} deletado(a) com sucesso.')
        return super().delete(request, *args, **kwargs)

