from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from backend.decorators import staff_required
from .models import *

@staff_required 
def faturas(request):
    faturas = Fatura.objects.select_related('cliente').all()

    return render(request, 'faturas.html', {
        'faturas': faturas
    })
