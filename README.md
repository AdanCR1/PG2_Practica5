# Práctica 5
# Patrones de diseño aplicados en componentes propios

## Descripción
En esta práctica se implementarán patrones de diseño en componentes propios de una aplicación. Se utilizarán los patrones de diseño **Singleton**, **Factory** y **Builder** para la estructura y funcionalidad del código.

## Estructura del proyecto

PG2_Practica5/
├── manage.py
├── requirements.txt
├── README.md
├── Api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── logger.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pedidos_cafe/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── base.py
│   ├── builder.py
│   ├── factory.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/

### Explicación de los patrones de diseño

## 1. Patrón Singleton

El patrón Singleton garantiza que una clase tenga una única instancia y proporciona un punto global de acceso a ella. Se utiliza para centralizar el registro de logs en la aplicación, evitando múltiples instancias de logger y asegurando un historial único de eventos.

**Implementado en:**  
Archivo: `Api/logger.py`

```python
class Logger:
    _instancia = None
    _logs = []

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def registrar(self, mensaje):
        self._logs.append(mensaje)

    def obtener_logs(self):
        return self._logs
```

# Usos del patrón Singleton:
Cada vez que se calcula el precio o ingredientes de un pedido, se registra un mensaje usando logger().registrar(mensaje).

---

## 2. Patrón Factory

El patrón Factory permite crear objetos sin exponer la lógica de creación al cliente y utiliza una interfaz común para instanciar objetos de diferentes tipos. Se usa para crear la base del café (espresso, americano, latte) según la selección del usuario.

**Implementado en:**  
Archivo: `pedidos_cafe/factory.py`
```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class FactoryProductos:
    @staticmethod
    def crear_producto(tipo, nombre, precio):
        if tipo == "comida":
            return ProductoComida(nombre, precio)
        elif tipo == "bebida":
            return ProductoBebida(nombre, precio)
        else:
            raise ValueError("Tipo de producto desconocido.")

class ProductoComida(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)

class ProductoBebida(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)
```

# Usos del patrón Factory:
En el serializador (pedidos_cafe/serializers.py), al calcular el precio o ingredientes finales, se llama a CafeFactory.obtener_base(obj.tipo_base). Así, la lógica de creación de la base del café está centralizada y desacoplada del resto del código.

---

## 3. Patrón Builder
El patrón Builder separa la construcción de un objeto complejo de su representación, permitiendo crear diferentes representaciones paso a paso. Se utiliza para construir cafés personalizados agregando ingredientes y eligiendo tamaño, calculando el precio final.

**Implementado en:**  
Archivo: `pedidos_cafe/builder.py`

```python
class CafePersonalizadoBuilder:
    # ...
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
```

# Usos del patrón Builder:
En el serializador (pedidos_cafe/serializers.py), se utiliza el builder y el director para construir el café personalizado y calcular el precio y los ingredientes finales.
Por ejemplo:
```bash
cafe = CafeFactory.obtener_base(obj.tipo_base)
builder = CafePersonalizadoBuilder(cafe)
director = CafeDirector(builder)
director.construir(obj.ingredientes, obj.tamanio)
precio = builder.obtener_precio()
```

----

## Archivo `pedidos_cafe/base.py`
El archivo base.py define las clases base para los tipos de café y es fundamental para el funcionamiento del patrón Factory y Builder. Aquí tienes el contenido correcto:

```python
class CafeBase:
    def __init__(self):
        self.ingredientes = []
        self.precio = 0

    def inicializar(self):
        raise NotImplementedError()

    def obtener_ingredientes_base(self):
        return self.ingredientes

    def precio_base(self):
        return self.precio

class Espresso(CafeBase):
    def inicializar(self):
        self.ingredientes = ["café concentrado"]
        self.precio = 10

class Americano(CafeBase):
    def inicializar(self):
        self.ingredientes = ["café filtrado", "agua caliente"]
        self.precio = 12

class Latte(CafeBase):
    def inicializar(self):
        self.ingredientes = ["café concentrado", "leche vaporizada", "espuma"]
```

# En conclusión:

Factory: Elige y crea la base del café según la selección del usuario, centralizando la lógica de creación.
Builder: Permite personalizar el café y calcular el precio final.
Singleton: Centraliza el registro de logs, asegurando un único punto de acceso y evitando múltiples instancias.
API: Permite crear y consultar pedidos de café personalizados de forma sencilla y estructurada.

---

## Extras:

- Se implementó una validación tanto para el panel de administración como para la API, asegurando que los ingredientes seleccionados sean válidos:

**Validación de ingredientes en el modelo PedidoCafe:**
```python
from django.core.exceptions import ValidationError
class PedidoCafe(models.Model):
    # ...
    def clean(self):
    validos = {"leche", "azúcar", "canela", "chocolate", "vainilla", "caramelo", "miel"}
    if not isinstance(self.ingredientes, list):
        raise ValidationError({"ingredientes": "deben ser una lista."})
    for ing in self.ingredientes:
        if ing not in validos:
            raise ValidationError({"ingredientes": f"ingrediente inválido: {ing}"})
```

***Validación de ingredientes en el serializador PedidoCafeSerializer:**
```python
from rest_framework import serializers
class PedidoCafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCafe
        fields = '__all__'

    def validate_ingredientes(self, value):
        validos = {"leche", "azúcar", "canela", "chocolate", "vainilla", "caramelo", "miel"}
        if not isinstance(value, list):
            raise serializers.ValidationError("Los ingredientes deben ser una lista.")
        for ing in value:
            if ing not in validos:
                raise serializers.ValidationError(f"Ingrediente inválido: {ing}")
        return value
```