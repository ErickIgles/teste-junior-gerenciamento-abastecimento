from django.contrib import messages
from django.shortcuts import redirect





class EmpresaPermissionMixin:
    """
    Restringe acesso aos funcionários da empresa ao usuário responsável pela empresa.
    """
    
    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()
        if obj.cargo.setor.empresa.usuario_responsavel != self.request.user:
            messages.error(request, 'Você não tem permissão para acessar este registro.')
            return redirect('home:index')

        return super().dispatch(request, *args, **kwargs)
    
    