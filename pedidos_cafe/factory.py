from .base import Espresso, Americano, Latte

class CafeFactory:
    @staticmethod
    def obtener_base(tipo_base):
        bases = {
            "espresso": Espresso,
            "americano": Americano,
            "latte": Latte
        }
        clase_base = bases.get(tipo_base)
        if clase_base is None:
            raise ValueError("Tipo de base no válida")
        instancia = clase_base()
        instancia.inicializar()
        return instancia