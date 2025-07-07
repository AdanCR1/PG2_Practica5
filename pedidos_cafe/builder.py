class CafePersonalizadoBuilder:
    PRECIO_INGREDIENTES_EXTRA = {
        "leche": 3,
        "azúcar": 1,
        "canela": 2,
        "chocolate": 4,
        "vainilla": 3,
        "caramelo": 3,
        "miel": 2,
    }

    MULTIPLICADOR_TAMANIO = {
        "pequeño": 1.0,
        "mediano": 1.2,
        "grande": 1.5,
    }

    def __init__(self, cafe_base):
        self.cafe = cafe_base
        self.ingredientes_extra = []
        self.tamanio = "mediano"

    def añadir_ingredientes(self, ingredientes):
        self.ingredientes_extra.extend(ingredientes)

    def establecer_tamanio(self, tamanio):
        self.tamanio = tamanio

    def obtener_precio(self):
        base = self.cafe.precio_base()
        extras = sum(self.PRECIO_INGREDIENTES_EXTRA.get(i, 0) for i in self.ingredientes_extra)
        return round((base + extras) * self.MULTIPLICADOR_TAMANIO.get(self.tamanio, 1.0), 2)

    def obtener_ingredientes_finales(self):
        return self.cafe.obtener_ingredientes_base() + self.ingredientes_extra

class CafeDirector:
    def __init__(self, builder):
        self.builder = builder

    def construir(self, ingredientes, tamanio):
        self.builder.añadir_ingredientes(ingredientes)
        self.builder.establecer_tamanio(tamanio)