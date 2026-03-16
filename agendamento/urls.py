from django.contrib import admin
from django.urls import path, include
from backend.views import erro_403
from django.contrib.auth import views as auth_views

handler403 = "backend.views.erro_403"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('', include('backend.urls')),
    path('', include('financeiro.urls')),

    # recuperação de senha
    path(
        "recuperar-senha/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset.html",
            email_template_name="mail/password_reset_email.html",
        ),
        name="password_reset",
    ),

    path(
        "recuperar-senha-enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset-concluido/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
