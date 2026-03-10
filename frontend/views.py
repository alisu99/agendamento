from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from backend.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from datetime import date, timedelta

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

    return render(request, "auth/login.html")


@login_required()
def historico(request):
    usuario = request.user
    historico = Agendamento.objects.filter(usuario=usuario).order_by('-id')

    context = {
        "historico": historico,
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
        hoje = date.today()
        limite = hoje + timedelta(days=10)

        if data_obj < hoje or data_obj > limite:
            return redirect("index")

        existe = Agendamento.objects.filter(
            quadra=quadra, horario=horario, data=data
        ).exists()

        if existe:
            return redirect("index")

        Agendamento.objects.create(
            usuario=request.user, quadra=quadra, horario=horario, data=data
        )

        return redirect("meus-agendamentos")

    context = {
        "quadras": quadras,
    }

    return render(request, "index.html", context)


@login_required
def cancelar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    if agendamento.usuario == request.user:
        agendamento.delete()
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


@login_required
def agendamentos(request):
    agendamentos = Agendamento.objects.all()

    context = {
        'agendamentos': agendamentos,
    }
    return render(request, 'admin/agendamentos.html', context)