from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class GroupRequiredMixin(AccessMixin):
    """
        Verifica o tipo de usuário e redireciona
        para tela de inicial e apresenta
        mensagem sobre permissão
    """
    group_required = []

    def dispatch(self, request, *args, **kwargs):

        usuario = request.user

        if not usuario.is_authenticated:
            return self.handle_no_permission()

        if usuario.is_staff or usuario.empresa():
            return super().dispatch(request, *args, **kwargs)


        grupo = usuario.groups.filter(name__in=self.group_required)

        if not grupo.exists():
            
            return self.handle_no_permission()


        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(
            self.request,
            'Você não tem permissão para acessar esta página.'
        )
        return redirect(reverse_lazy('home:index'))
