from django.contrib import admin
from .models import PedidoCafe

@admin.register(PedidoCafe)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "tipo_base", "tamanio", "fecha")
    readonly_fields = ("fecha",)