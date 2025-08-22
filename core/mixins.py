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

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        if request.user.is_empresa():
            return super().dispatch(request, *args, **kwargs)

        is_in_group = False

        for group_name in self.group_required:
            if request.user.groups.filter(name=group_name).exists():
                is_in_group = True
                break

        if not is_in_group:
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
