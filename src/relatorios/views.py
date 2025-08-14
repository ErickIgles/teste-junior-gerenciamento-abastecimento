from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from cadastros.tanques.models import Tanque
from cadastros.abastecimento.models import RegistroAbastecimento

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from cadastros.funcionarios.models import Funcionario



class RelatorioAbastecimento(LoginRequiredMixin, ListView):
    template_name = 'abastecimentos/relatorio.html'
    model = RegistroAbastecimento



    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tanques = Tanque.objects.all()

        tanques_com_registro = []

        for tanque in tanques:

            if RegistroAbastecimento.objects.filter(tanque=tanque).exists():
                tanques_com_registro.append(tanque)            

        context['tanques_com_registro'] = tanques_com_registro
        return context


class RelatorioAbastecimentoDetalhe(LoginRequiredMixin, DetailView):
    template_name = 'abastecimentos/detalhe.html'
    model = Tanque
    context_object_name = 'tanque'


    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user

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



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tanque = self.get_object()
        registros_tanque = RegistroAbastecimento.objects.filter(tanque=tanque).order_by('criado')

        soma_valores = 0

        for registro in registros_tanque:
            soma_valores += registro.valor_total_abastecimento


        context.update({
            'registros_tanque': registros_tanque,  # Todos os registros do tanque
            'soma_valores': soma_valores,  # A soma total dos valores de abastecimento
        })

        return context

