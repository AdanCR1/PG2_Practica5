from django.db import models
from django.core.exceptions import ValidationError

class PedidoCafe(models.Model):
    BASE_CHOICES = [
        ("espresso", "Espresso"),
        ("americano", "Americano"),
        ("latte", "Latte"),
    ]

    TAMANIO_CHOICES = [
        ("pequeño", "Pequeño"),
        ("mediano", "Mediano"),
        ("grande", "Grande"),
    ]

    cliente = models.CharField(max_length=100, help_text="Nombre del cliente", null=True, blank=True)
    tipo_base = models.CharField(max_length=20, choices=BASE_CHOICES)
    ingredientes = models.JSONField(default=list, help_text="leche, azúcar, canela, chocolate, vainilla, caramelo, miel", blank=True, null=True)
    tamanio = models.CharField(max_length=10, choices=TAMANIO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.cliente} - {self.tipo_base} ({self.tamanio})"
    
    def clean(self):
        validos = {"leche", "azúcar", "canela", "chocolate", "vainilla", "caramelo", "miel"}
        if not isinstance(self.ingredientes, list):
            raise ValidationError({"ingredientes": "deben ser una lista."})
        for ing in self.ingredientes:
            if ing not in validos:
                raise ValidationError({"ingredientes": f"ingrediente inválido: {ing}"})