import conexion
from models.informe import Informe

if __name__ == '__main__':

    conexion.Conexion.conexion()

    Informe.generar_informe_clientes()
    # nforme.generar_informe_vehiculos()

    print("Informe generado")
