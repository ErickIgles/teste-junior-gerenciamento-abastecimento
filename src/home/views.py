from django.views.generic import TemplateView
from django.shortcuts import render


class IndexTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):

        usuario_grupo = request.user.groups.filter(
            name__in=[
                'gerente_geral',
                'administradores'
            ]
        ).exists()
        if usuario_grupo:
            return render(
                request,
                'base.html',
                {'usuario_grupo': usuario_grupo}
            )
        return render(
            request,
            'base.html'
        )
