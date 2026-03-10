from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from backend.models import *
from django.contrib.auth.decorators import login_required


@login_required()
def historico(request):
    usuario = request.user
    historico = Agendamento.objects.filter(usuario=usuario)

    context = {
        'historico': historico,
    }

    return render(request, 'historico.html', context)


@login_required
def index(request):
    quadras = Quadra.objects.all()
    horarios = Horario.objects.all()

    if request.method == "POST":

        data = request.POST.get("data")
        quadra_id = request.POST.get("quadra")
        horario_id = request.POST.get("horario")

        quadra = Quadra.objects.get(id=quadra_id)
        horario = Horario.objects.get(id=horario_id)

        Agendamento.objects.create(
            usuario=request.user,
            quadra=quadra,
            horario=horario,
            data=data
        )

        return redirect("meus-agendamentos")

    context = {
        "quadras": quadras,
        "horarios": horarios,
    }

    return render(request, "index.html", context)


@login_required
def cancelar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    if agendamento.usuario == request.user:
        agendamento.delete()
    return redirect('meus-agendamentos')


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
        lista.append({
            "id": h.id,
            "inicio": h.hora_inicio.strftime("%H:%M"),
            "fim": h.hora_fim.strftime("%H:%M")
        })

    return JsonResponse(lista, safe=False)