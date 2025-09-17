from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from cadastros.funcionarios.models import Funcionario

from cadastros.empresas.models import Empresa


class EmpresaRelatorioPermissionMixin:
    """
    Mixin para verificar se o relatório pertence à empresa
    do usuário logado.
    """

    def get_empresa_usuario(self, usuario):
        if usuario.is_empresa():
            return Empresa.objects.get(usuario_responsavel=usuario)
        return Funcionario.objects.select_related("empresa").get(user=usuario).empresa

    def get_empresa_do_objeto(self):
        """
        Deve ser implementado na view filha para retornar
        a empresa do objeto/relatório.
        """
        raise NotImplementedError("Implemente 'get_empresa_do_objeto' na view filha.")

    def dispatch(self, request, *args, **kwargs):
        usuario_logado = request.user
        empresa_usuario = self.get_empresa_usuario(usuario_logado)
        empresa_obj = self.get_empresa_do_objeto()

        if not empresa_obj or empresa_usuario != empresa_obj:
            messages.error(request, "Você não tem permissão para acessar este relatório.")
            return redirect("home:index")

        return super().dispatch(request, *args, **kwargs)