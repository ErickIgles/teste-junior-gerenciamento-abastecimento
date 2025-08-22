from django.contrib import messages
from django.shortcuts import redirect

from ..models import Funcionario


class EmpresaPermissionMixin:
    """
        Restringe acesso aos funcionários
        da empresa ao usuário responsável pela empresa.
    """

    def dispatch(self, request, *args, **kwargs):

        usuario = Funcionario.objects.get(
            user=request.user
        )

        obj = self.get_object()
        if obj.empresa.usuario_responsavel != usuario.empresa.usuario_responsavel:
            messages.error(
                request,
                'Você não tem permissão para acessar este registro.'
            )
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
