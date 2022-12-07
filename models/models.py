class Cliente:

    def __init__(self, dni: str, nombre: str, alta: str, direccion: str, provincia: str, municipio: str, pago: str ):

        self.dni = dni
        self.nombre = nombre
        self.alta = alta
        self.direccion = direccion
        self.provincia = provincia
        self.municipio = municipio
        self.pago = pago


class Coche:

    def __init__(self, matricula: str, dnicli: str, marca: str, modelo: str, motor: str):

        self.matricula = matricula
        self.dnicli = dnicli
        self.marca = marca
        self.modelo = modelo
        self.motor = motor
