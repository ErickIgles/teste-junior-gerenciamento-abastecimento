from django.shortcuts import redirect
from django.contrib import messages


class EmpresaPermissionMixin:

    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()

        if obj.usuario_responsavel != self.request.user:
            messages.error(
                request,
                'Você não possui permissão para acessar este registro.'
            )
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin:

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.username != self.request.user.username:
            messages.error(
                request,
                'Você não tem permissão para acesar esse registro.'
            )
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
