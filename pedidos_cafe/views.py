from rest_framework import generics
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.serializers import PedidoCafeSerializer

class CrearPedidoCafeView(generics.CreateAPIView):
    queryset = PedidoCafe.objects.all()
    serializer_class = PedidoCafeSerializer
class PedidoCafeListView(generics.ListAPIView):
    queryset = PedidoCafe.objects.all()
    serializer_class = PedidoCafeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        cliente = self.request.query_params.get('cliente', None)
        if cliente:
            queryset = queryset.filter(cliente__icontains=cliente)
        return queryset