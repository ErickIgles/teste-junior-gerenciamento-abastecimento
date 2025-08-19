from django.shortcuts import redirect
from django.contrib import messages




class EmpresaTanquePermissionMixin:

    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()

        if obj.empresa.usuario_responsavel != request.user:
            messages.error(request, 'Você não possui permissão para acessar este registro.')
            return redirect('home:index')

        return super().dispatch(request, *args, **kwargs)
    
    