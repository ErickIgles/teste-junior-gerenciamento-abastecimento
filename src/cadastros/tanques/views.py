from django.urls import reverse_lazy

from django.shortcuts import redirect
from django.core.paginator import Paginator

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tanque
from .forms import TanqueForm

from django.contrib.auth.models import Group
from cadastros.funcionarios.models import Funcionario


class TanqueCadastroView(LoginRequiredMixin, CreateView):
    model = Tanque
    form_class = TanqueForm
    template_name = 'tanques/tanque_form.html'
    success_url = reverse_lazy('cadastros:tanques:listar')

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


class TanqueListarView(LoginRequiredMixin, ListView):
    model = Tanque
    context_object_name = 'tanques'
    template_name = 'tanques/tanque_lista.html'

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


class TanqueAtualizarView(LoginRequiredMixin, UpdateView):
    model = Tanque
    form_class = TanqueForm
    context_object_name = 'tanque'
    template_name = 'tanques/tanque_form_atualizar.html'
    success_url = reverse_lazy('cadastros:tanques:listar')


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




class TanqueDeletarView(LoginRequiredMixin, DeleteView):
    model = Tanque
    context_object_name = 'tanque'
    template_name = 'tanques/tanque_form_delete.html'
    success_url = reverse_lazy('cadastros:tanques:listar')    


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
        