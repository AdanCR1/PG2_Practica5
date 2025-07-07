from django.urls import path
from .views import PedidoCafeListView, CrearPedidoCafeView

urlpatterns = [
    path('pedidos/', PedidoCafeListView.as_view(), name="lista-pedidos"),
    path('pedidos/crear/', CrearPedidoCafeView.as_view(), name="crear-pedido"),
]