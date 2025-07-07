from rest_framework import serializers
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.factory import CafeFactory
from pedidos_cafe.builder import CafePersonalizadoBuilder, CafeDirector
from Api.logger import Logger


class PedidoCafeSerializer(serializers.ModelSerializer):
    precio_total = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()

    class Meta:
        model = PedidoCafe
        fields = [
            "id",
            "cliente",
            "tipo_base",
            "ingredientes",
            "tamanio",
            "fecha",
            "precio_total",
            "ingredientes_finales",
        ]

    def validate_ingredientes(self, value):
        validos = {"leche", "azúcar", "canela", "chocolate", "vainilla", "caramelo", "miel"}
        if not all(ing in validos for ing in value):
            raise serializers.ValidationError("Ingrediente inválido")
        return value

    def get_precio_total(self, obj):
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        Logger().registrar(f"Se calculó el precio del pedido {obj.id}")
        return builder.obtener_precio()

    def get_ingredientes_finales(self, obj):
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        Logger().registrar(f"Se listaron ingredientes finales del pedido {obj.id}")
        return builder.obtener_ingredientes_finales()
