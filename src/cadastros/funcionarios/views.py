from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView


from django.core.paginator import Paginator

from django.urls import reverse_lazy
from .forms import UserForm, UserUpdateForm



class FuncionarioCadastrarView(CreateView):
    template_name = 'funcionarios/form_register.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('cadastros:funcionarios:listar')

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class FuncionarioListarView(ListView):
    template_name = 'funcionarios/lista_funcionario.html'
    model = User
    context_object_name = 'funcionarios'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('p')
        
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(username__icontains=q)
            queryset = queryset.filter(email__icontains=q)
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
    

class FuncionarioAtualizarView(UpdateView):
    template_name = 'funcionarios/form_update.html'
    model = User
    context_object_name = 'funcionario'
    form_class = UserUpdateForm
    success_url = reverse_lazy('cadastros:funcionarios:listar')


class FuncionarioDeletarView(DeleteView):
    template_name = 'funcionarios/form_delete.html'
    model = User
    context_object_name = 'funcionario'
    success_url = reverse_lazy('cadastros:funcionarios:listar')

