from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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