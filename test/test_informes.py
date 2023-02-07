import conexion
from models.informe import Informe
from models.factura import Factura

if __name__ == '__main__':

    conexion.Conexion.conexion()

    factura = Factura(34, "35643562F", "45645trt", "25/07/2023")

    Informe.generar_informe_factura(factura)

    print("Informe generado")
