import conexion
from models.informe import Informe
from models.factura import Factura

if __name__ == '__main__':

    conexion.Conexion.conexion()


    Informe.generar_informe_clientes()

    print("Informe generado")
