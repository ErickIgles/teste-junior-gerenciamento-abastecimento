import io
from decimal import Decimal


from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice

import qrcode

from cadastros.tanques.models import Tanque
from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario
from cadastros.fornecedores.models import Fornecedor

from ..models import RegistroReabastecimento
from .helpers import reverter_reabastecimento, ajustar_next_url


def gerador_qr(request):

    usuario = request.user

    if not usuario.is_authenticated:

        return HttpResponse('Não autenticado', status=401)

    dispositivo, criado = TOTPDevice.objects.get_or_create(
        user=usuario,
        name='default'
    )

    uri = dispositivo.config_url

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type="image/png")


def validacao_token_criar_reabastecimento(request):

    usuario = request.user

    if request.method == 'POST':

        token = request.POST.get('token')

        try:
            dispositivo = TOTPDevice.objects.get(user=usuario, name='default')

        except TOTPDevice.DoesNotExist:

            messages.error(
                request,
                'Dispositivo não configurado.'
            )

            return render(
                request,
                'validacao.html'
            )

        verifica_token = dispositivo.verify_token(token)

        if verifica_token:

            dados = request.session.pop('abastecimento_tanque_form', None)

            if dados:

                try:

                    tanque = Tanque.objects.get(id=dados['tanque_id'])

                    quantidade = Decimal(dados['quantidade'])

                    fornecedor_id = dados['fornecedor_id']

                    fornecedor = Fornecedor.objects.get(
                        pk=fornecedor_id
                    )

                    if usuario.is_empresa():

                        empresa = Empresa.objects.get(
                            usuario_responsavel=usuario
                        )

                        reabastecimento = RegistroReabastecimento.objects.create(
                            tanque=tanque,
                            quantidade=quantidade,
                            empresa=empresa,
                            fornecedor=fornecedor
                        )

                    else:
                        funcionario = Funcionario.objects.get(
                            user=usuario
                        )

                        reabastecimento = RegistroReabastecimento.objects.create(
                            tanque=tanque,
                            quantidade=quantidade,
                            funcionario=funcionario,
                            empresa=funcionario.empresa,
                            fornecedor=fornecedor
                        )

                    reabastecimento.aplicar_reabastecimento()

                    messages.success(
                        request,
                        f'Tanque {tanque.identificador_tanque} reabastecido.'
                    )

                    next_url = request.session.pop('next', None)

                    if next_url:

                        next_url = ajustar_next_url(next_url)

                        return redirect(next_url)

                    return redirect(
                        reverse(
                            'servicos:abastecimento:listar_reabastecimento'
                        )
                    )

                except Tanque.DoesNotExist:

                    messages.error(
                        request,
                        'Tanque não encontrado'
                    )

                    return render(
                        request,
                        'validacao.html'
                    )
            else:

                messages.error(
                    request,
                    'Dados da sessão não encontrados'
                )

                return render(
                    request,
                    'validacao.html'
                )
        else:
            messages.error(
                request,
                'Código inválido'
            )

            return render(
                request,
                'validacao.html'
            )

    return render(
        request,
        'validacao.html'
    )


def validacao_token_deletar_reabastecimento(request):

    usuario = request.user

    if request.method == 'POST':

        token = request.POST.get('token')

        try:

            dispositivo = TOTPDevice.objects.get(user=usuario, name='default')

        except TOTPDevice.DoesNotExist:

            messages.error(
                request,
                'Dispositivo não configurado.'
            )

            return render(
                request,
                'validacao.html'
            )

        valida_token = dispositivo.verify_token(token)

        if valida_token:

            pk = request.session.pop('registro_a_deletar', None)

            if not pk:

                messages.error(
                    request,
                    'Registro não encontrado'
                )
                return render(
                    request,
                    'validacao.html'
                )

            try:

                obj = RegistroReabastecimento.objects.get(
                    id=pk
                )

                reverter_reabastecimento(obj)

                obj.delete()

                messages.success(
                    request,
                    'Registro deletado com sucesso.'
                )

                next_url = request.session.pop('next', None)

                if next_url:

                    next_url = ajustar_next_url(next_url)

                    return redirect(next_url)

                return redirect(
                    reverse('servicos:abastecimento:listar_reabastecimento')
                )

            except RegistroReabastecimento.DoesNotExist:

                messages.error(
                    request,
                    'Registro não encontrado.'
                )

                return render(
                    request,
                    'validacao.html'
                )

        else:

            messages.error(
                request,
                'Código inválido'
            )

    return render(
        request,
        'validacao.html'
    )


def pagina_qr(request):

    return render(request, 'qrcode.html')
