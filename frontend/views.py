from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from backend.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from datetime import date, timedelta
from backend.decorators import *
from django.utils import timezone
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.conf import settings


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")



def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Email ou senha inválidos.")

    return render(request, "auth/login.html")


@login_required()
def historico(request):
    usuario = request.user

    historico = (
        Agendamento.objects
        .filter(usuario=usuario)
        .select_related("quadra", "horario")
        .order_by("-data", "-hora_inicio")
    )

    hoje = timezone.now().date()

    context = {
        "historico": historico,
        "hoje": hoje,
    }

    return render(request, "historico.html", context)


@login_required
def index(request):

    quadras = Quadra.objects.all()

    if request.method == "POST":

        data = request.POST.get("data")
        quadra_id = request.POST.get("quadra")
        horario_id = request.POST.get("horario")

        quadra = get_object_or_404(Quadra, id=quadra_id)
        horario = get_object_or_404(Horario, id=horario_id)

        data_obj = date.fromisoformat(data)

        descanso = Descanso.objects.first()

        if descanso and descanso.dias_semana:

            mapa = {
                "mon": "seg",
                "tue": "ter",
                "wed": "qua",
                "thu": "qui",
                "fri": "sex",
                "sat": "sab",
                "sun": "dom",
            }

            dia_semana = mapa[data_obj.strftime("%a").lower()]

            if dia_semana in descanso.dias_semana:
                return redirect("index")
        hoje = date.today()
        limite = hoje + timedelta(days=10)

        if data_obj < hoje or data_obj > limite:
            return redirect("index")

        existe = Agendamento.objects.filter(
            quadra=quadra,
            horario=horario,
            data=data
        ).exists()
        

        if existe:
            return redirect("index")

        agendamento = Agendamento.objects.create(
            usuario=request.user,
            quadra=quadra,
            horario=horario,
            data=data,
            quadra_nome=quadra.apelido,
            quadra_numero=quadra.numeracao,
            hora_inicio=horario.hora_inicio,
            hora_fim=horario.hora_fim,
        )

        agendamento.save()

        # html_content = render_to_string(
        #     "mail/agendamento-confirmado.html",
        #     {
        #         "nome": agendamento.usuario.first_name,
        #         "quadra": agendamento.quadra_nome,
        #         "numeracao": agendamento.quadra.numeracao,
        #         "data": agendamento.data,
        #         "hora_inicio": agendamento.hora_inicio,
        #         "hora_fim": agendamento.hora_fim,
        #         "url_sistema": request.build_absolute_uri("/"),
        #         "ano": datetime.now().year
        #     }
        # )

        # email = EmailMultiAlternatives(
        #     subject="Agendamento confirmado - Arena Vila Sol",
        #     body=f"""
        # Olá {agendamento.usuario.first_name},

        # Seu agendamento foi confirmado!

        # Quadra: {agendamento.quadra_nome} - {agendamento.quadra.numeracao}
        # Data: {agendamento.data}
        # Horário: {agendamento.hora_inicio} às {agendamento.hora_fim}

        # Acesse o sistema para ver seus agendamentos.
        # """,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[agendamento.usuario.email]
        # )

        # email.attach_alternative(html_content, "text/html")
        # email.send()

        return redirect("meus-agendamentos")

    context = {
        "quadras": quadras,
    }

    return render(request, "index.html", context)


@login_required
def cancelar_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
        usuario=request.user
    )

    agendamento.delete()

#     html_content = render_to_string(
#         "mail/agendamento-cancelado.html",
#         {
#             "nome": agendamento.usuario.first_name,
#             "quadra": agendamento.quadra_nome,
#             "numeracao": agendamento.quadra.numeracao,
#             "data": agendamento.data,
#             "hora_inicio": agendamento.hora_inicio,
#             "hora_fim": agendamento.hora_fim,
#             "url_sistema": request.build_absolute_uri("/"),
#             "ano": datetime.now().year
#         }
#     )

#     email = EmailMultiAlternatives(
#         subject="Agendamento Cancelado",
#         body=f"""
# Olá {agendamento.usuario.first_name},

# Seu agendamento foi cancelado.

# Quadra: {agendamento.quadra_nome}
# Data: {agendamento.data}
# Horário: {agendamento.hora_inicio} às {agendamento.hora_fim}
# """,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[agendamento.usuario.email]
#     )

#     email.attach_alternative(html_content, "text/html")

#     try:
#         email.send()
#     except:
#         pass

    return redirect("meus-agendamentos")

@login_required
def horarios_disponiveis(request):
    data = request.GET.get("data")
    quadra = request.GET.get("quadra")
    horarios = Horario.objects.all()
    agendados = Agendamento.objects.filter(
        data=data,
        quadra_id=quadra,
    ).values_list("horario_id", flat=True)

    horarios_livres = horarios.exclude(id__in=agendados)

    lista = []

    for h in horarios_livres:
        lista.append(
            {
                "id": h.id,
                "inicio": h.hora_inicio.strftime("%H:%M"),
                "fim": h.hora_fim.strftime("%H:%M"),
            }
        )

    return JsonResponse(lista, safe=False)


def verificar_descanso(request):

    data = request.GET.get("data")

    if not data:
        return JsonResponse({"descanso": False})

    data_obj = date.fromisoformat(data)

    descanso = Descanso.objects.first()

    if not descanso or not descanso.dias_semana:
        return JsonResponse({"descanso": False})

    mapa = {
        "mon": "seg",
        "tue": "ter",
        "wed": "qua",
        "thu": "qui",
        "fri": "sex",
        "sat": "sab",
        "sun": "dom",
    }

    dia_semana = mapa[data_obj.strftime("%a").lower()]

    if dia_semana in descanso.dias_semana:
        return JsonResponse({"descanso": True})

    return JsonResponse({"descanso": False})