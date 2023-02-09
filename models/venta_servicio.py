

class VentaServicio:

    def __init__(self, unidades: int, concepto: str, precio_unidad: float):

        self.unidades = unidades
        self.concepto = concepto
        self.precio_unidad = precio_unidad
        self.subtotal = float(precio_unidad) * unidades
