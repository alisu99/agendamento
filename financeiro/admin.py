from django.contrib import admin
from .models import Fatura


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'cliente',
        'valor',
        'referencia',
        'data_vencimento',
        'data_pagamento',
        'status_formatado',
    )

    list_filter = (
        'status',
        'data_vencimento',
        'data_pagamento',
    )

    search_fields = (
        'titulo',
        'referencia',
        'cliente__username',
        'cliente__email',
    )

    ordering = ('-data_vencimento',)

    list_per_page = 20

    autocomplete_fields = ['cliente']

    readonly_fields = ('status_formatado',)

    fieldsets = (
        ('Informações da Fatura', {
            'fields': ('titulo', 'cliente', 'valor', 'referencia')
        }),
        ('Datas', {
            'fields': ('data_vencimento', 'data_pagamento')
        }),
        ('Status', {
            'fields': ('status', 'status_formatado')
        }),
    )

    def status_formatado(self, obj):
        if obj.data_pagamento:
            return "Pago"
        elif obj.status == 'cancelado':
            return "Cancelado"
        return "Pendente"

    status_formatado.short_description = "Status"