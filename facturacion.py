import conexion
from ventMain import Ui_mainWindow
from PyQt6 import QtWidgets, QtCore


class TabFacturacion:

    def __init__(self, ui: Ui_mainWindow):

        self.ui = ui
        self.conceptos : list[QtWidgets.QComboBox] = []

        facturacion_header = self.ui.tabSeleccionClientes.horizontalHeader()
        facturacion_header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(facturacion_header, 0).Stretch)

        ventas_header = self.ui.tabVentas.horizontalHeader()
        ventas_header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(ventas_header, 0).Stretch)

        self.cargar_linea_venta()

        # Cargar conceptos a medida que se crean o destruyen
        self.ui.btnGuardarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnEliminarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnModificarServ.clicked.connect(self.__cargar_conceptos)

        # Botones del apartado de facturación
        # self.ui.btnSeleccionarCliente.clicked.connect()

    def cargar_linea_venta(self):

        try:

            index = 4

            tab_ventas = self.ui.tabVentas
            tab_ventas.setRowCount(index + 1)

            lista_conceptos = conexion.Conexion.cargar_lista_conceptos()
            lista_conceptos.insert(0, "")

            for i in range(index):

                cmb_servicio = QtWidgets.QComboBox()
                txt_unidades = QtWidgets.QLineEdit()

                txt_unidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                tab_ventas.setCellWidget(i, 0, cmb_servicio)
                tab_ventas.setItem(i, 2, QtWidgets.QTableWidgetItem(str("")))

                cmb_servicio.addItems(lista_conceptos)
                cmb_servicio.currentIndexChanged.connect(self.__recargar_precios_servicios)

                self.conceptos.append(cmb_servicio)

        except Exception as error:

            print("Error al cargar la línea de ventas", error)

    def __cargar_conceptos(self):

        try:

            lista_conceptos = conexion.Conexion.cargar_lista_conceptos()
            lista_conceptos.insert(0, "")

            for cmb in self.conceptos:

                cmb.clear()
                cmb.addItems(lista_conceptos)

        except Exception as error:

            print("Error al cargar la lista de conceptos", error)

    def __recargar_precios_servicios(self):

        try:

            tab_ventas = self.ui.tabVentas
            precio_total = 0.0

            for i, cmb in enumerate(self.conceptos):

                if cmb.currentText() == "":

                    tab_ventas.setItem(i, 1, QtWidgets.QTableWidgetItem(str("")))

                else:

                    precio = conexion.Conexion.obtener_precio_servicio_por_concepto(cmb.currentText())

                    tab_ventas.setItem(i, 1, QtWidgets.QTableWidgetItem(str(precio)))
                    tab_ventas.setItem(i, 2, QtWidgets.QTableWidgetItem(str("1")))
                    tab_ventas.setItem(i, 3, QtWidgets.QTableWidgetItem(str(precio)))

                    tab_ventas.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    precio_total += float(precio.replace(",", "."))

            self.ui.lblPrecioTotal.setText(str(precio_total))

        except Exception as error:

            print("Error al cargar el precio del servicio", error)

    def limpiar_facturas(self):

        pass