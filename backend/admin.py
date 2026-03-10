from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Quadra, Horario, Agendamento


# ==============================
# USER ADMIN
# ==============================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "cpf",
        "data_nasc",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cpf",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ("cpf", "data_nasc")
        }),
    )



# ==============================
# QUADRA ADMIN
# ==============================

@admin.register(Quadra)
class QuadraAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "apelido",
        "numeracao",
    )

    search_fields = (
        "apelido",
        "numeracao",
    )



# ==============================
# HORARIO ADMIN
# ==============================
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "hora_inicio",
        "hora_fim",
    )

    list_filter = (
        "hora_inicio",
    )

    search_fields = (
        "hora_inicio",
        "hora_fim",
    )


# ==============================
# AGENDAMENTO ADMIN
# ==============================

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "quadra",
        "horario",
        "data",
    )

    list_filter = (
        "quadra",
        "data",
    )

    search_fields = (
        "usuario__username",
        "usuario__cpf",
        "quadra__apelido",
    )

    autocomplete_fields = (
        "usuario",
        "quadra",
        "horario",
    )

    ordering = ("-data",)