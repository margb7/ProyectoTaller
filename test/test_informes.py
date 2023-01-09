
from models.informe import Informe

if __name__ == '__main__':

    Informe.generar_informe_clientes()
    Informe.generar_informe_vehiculos()

    print("Informe generado")
