from django.shortcuts import redirect
from django.contrib import messages

from cadastros.funcionarios.models import Funcionario


class EmpresaRelatorioPermissionMixin:

    """
    Mixin para comparar se o relatorio pertence a empresa
    que está tentando acessar.
    """

    def dispatch(self, request, *args, **kwargs):

        usuario_logado = self.request.user
        obj = self.get_object()

        if usuario_logado.is_empresa():
            if obj.empresa.usuario_responsavel != usuario_logado:
                messages.error(
                    request,
                    'Você não tem permissão para acessar este registro.'
                )
                return redirect('home:index')

        else:
            usuario_funcionario = Funcionario.objects.get(
                user=usuario_logado
            )

            if obj.empresa.usuario_responsavel != usuario_funcionario.empresa.usuario_responsavel:
                messages.error(
                    request,
                    'Você não tem permissão para acessar este registro.'
                )
                return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
