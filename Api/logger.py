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