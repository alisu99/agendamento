from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import *
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from django.utils import timezone


User = get_user_model()

def erro_403(request, exception):
    return render(request, "admin/403.html", status=403)

def criar_conta(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        data_nasc = request.POST.get("data_nasc")
        password = request.POST.get("password")
        telefone = request.POST.get("telefone")

        if User.objects.filter(email=email).exists():
            return redirect("criar_conta")

        if User.objects.filter(cpf=cpf).exists():
            return redirect("criar_conta")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            cpf=cpf,
            data_nasc=data_nasc,
            telefone=telefone,
        )
        return redirect("login")

    return render(request, "auth/criar_conta.html")

@login_required
def meu_perfil(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.telefone = request.POST.get("telefone")
        user.cpf = request.POST.get("cpf")
        user.data_nasc = request.POST.get("data_nasc")
        password = request.POST.get("password")

        if password:
            user.set_password(password)

        user.save()
        return redirect("meu-perfil")

    return render(request, "perfil.html")


@staff_required
def usuarios(request):

    busca = request.GET.get("busca")
    staff = request.GET.get("staff")

    usuarios = User.objects.all().order_by("-id")

    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) |
            Q(first_name__icontains=busca) |
            Q(last_name__icontains=busca) |
            Q(email__icontains=busca)
        )

    if staff == "sim":
        usuarios = usuarios.filter(is_staff=True)

    if staff == "nao":
        usuarios = usuarios.filter(is_staff=False)

    paginator = Paginator(usuarios, 10)
    page = request.GET.get("page")

    usuarios = paginator.get_page(page)

    context = {
        "usuarios": usuarios,
        "busca": busca,
        "staff": staff,
    }

    return render(request, "admin/usuarios.html", context)


@staff_required
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":

        usuario.first_name = request.POST.get("first_name")
        usuario.last_name = request.POST.get("last_name")
        usuario.telefone = request.POST.get("telefone")
        usuario.cpf = request.POST.get("cpf")
        usuario.data_nasc = request.POST.get("data_nasc")
        usuario.email = request.POST.get("email")

        usuario.is_active = "is_active" in request.POST
        usuario.is_staff = "is_staff" in request.POST

        password = request.POST.get("password")

        if password:
            usuario.set_password(password)

        usuario.save()

        return redirect("usuarios")

    context = {
        "usuario": usuario,
    }

    return render(request, "admin/editar-usuario.html", context)

@staff_required
def novo_usuario(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        is_active = "is_active" in request.POST
        is_staff = "is_staff" in request.POST

        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.is_active = is_active
        usuario.is_staff = is_staff

        usuario.save()
        return redirect("usuarios")

    return render(request, "admin/novo-usuario.html")


@staff_required
def excluir_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    return redirect('usuarios')

@staff_required
def agendamentos(request):
    agendamentos = (
        Agendamento.objects
        .select_related("usuario")
        .all()
        .order_by("-data", "-hora_inicio")
    )

    hoje = timezone.now().date()

    context = {
        "agendamentos": agendamentos,
        "hoje": hoje,
    }

    return render(request, "admin/agendamentos.html", context)


from django.http import JsonResponse

@staff_required
def ajustes(request):

    if request.method == "POST":

        action = request.POST.get("action")

        # ----------------
        # DELETE HORARIO
        # ----------------
        if action == "delete_hora":
            Horario.objects.filter(id=request.POST.get("id")).delete()
            return JsonResponse({"status": "ok"})

        # ----------------
        # ADD HORARIO
        # ----------------
        if action == "add_hora":
            inicio = request.POST.get("inicio")
            fim = request.POST.get("fim")

            hora = Horario.objects.create(
                hora_inicio=inicio,
                hora_fim=fim
            )

            return JsonResponse({
                "status": "ok",
                "id": hora.id,
                "inicio": hora.hora_inicio,
                "fim": hora.hora_fim
            })

        # ----------------
        # DELETE QUADRA
        # ----------------
        if action == "delete_quadra":
            Quadra.objects.filter(id=request.POST.get("id")).delete()
            return JsonResponse({"status": "ok"})

        # ----------------
        # ADD QUADRA
        # ----------------
        if action == "add_quadra":
            apelido = request.POST.get("apelido")
            numeracao = request.POST.get("numeracao")

            quadra = Quadra.objects.create(
                apelido=apelido,
                numeracao=numeracao
            )

            return JsonResponse({
                "status": "ok",
                "id": quadra.id,
                "apelido": quadra.apelido,
                "numeracao": quadra.numeracao
            })

        # ----------------
        # UPDATE NORMAL
        # ----------------

        # atualizar horarios
        ids = request.POST.getlist("hora_id[]")
        inicios = request.POST.getlist("hora_inicio[]")
        fins = request.POST.getlist("hora_fim[]")

        for i in range(len(ids)):
            Horario.objects.filter(id=ids[i]).update(
                hora_inicio=inicios[i],
                hora_fim=fins[i]
            )

        # atualizar quadras
        quadra_ids = request.POST.getlist("quadra_id[]")
        apelidos = request.POST.getlist("apelido[]")
        numeros = request.POST.getlist("numeracao[]")

        for i in range(len(quadra_ids)):
            Quadra.objects.filter(id=quadra_ids[i]).update(
                apelido=apelidos[i],
                numeracao=numeros[i]
            )

        return redirect("ajustes")

    context = {
        "horarios": Horario.objects.all(),
        "quadras": Quadra.objects.all()
    }

    return render(request, "admin/ajustes/ajustes.html", context)