import conexion
import events
import views.dialog_seleccionar_cliente

from models.factura import Factura
from models.informe import Informe

from ventMain import Ui_mainWindow
from PyQt6 import QtWidgets, QtCore


class TabFacturacion:

    def __init__(self, ui: Ui_mainWindow):

        self.ui = ui
        self.conceptos: list[QtWidgets.QComboBox] = []
        self.dlg_seleccionar_cliente = views.dialog_seleccionar_cliente.DialogSeleccionarCliente()
        self.factura = None

        facturacion_header = self.ui.tabSeleccionClientes.horizontalHeader()
        facturacion_header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(facturacion_header, 0).Stretch)

        self.ui.tabVentas.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.ui.tabVentas.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)

        ventas_header = self.ui.tabVentas.horizontalHeader()
        ventas_header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(ventas_header, 0).Stretch)

        ventas_header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.cargar_linea_venta(1)

        # Cargar conceptos a medida que se crean o destruyen
        self.ui.btnGuardarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnEliminarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnModificarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnSeleccionarCliente.clicked.connect(self.dlg_seleccionar_cliente.show)
        self.ui.btnImprimirFactura.clicked.connect(self.imprimir_factura)

        self.dlg_seleccionar_cliente.ui.btnAceptarCliente.clicked.connect(self.seleccionar_cliente)
        self.ui.btnLimpiarFact.clicked.connect(self.limpiar_facturas)

    def imprimir_factura(self):

        try:

            # TODO: temp

            factu = Factura(4, "35611422Q", "rte3451", "25/07/2023")

            Informe.generar_informe_factura(factu)
            return

            if self.factura is None:

                events.Eventos.lanzar_error("No se ha seleccionado una factura")

            else:

                pass

        except Exception as error:

            print("Error al imprimir factura", error)

    def seleccionar_cliente(self):

        try:

            cliente = conexion.Conexion.one_cli(self.dlg_seleccionar_cliente.cliente)

            if cliente is not None:

                self.ui.txtFactDni.setText(cliente.dni)
                self.ui.txtProvinciaFact.setText(cliente.provincia)

        except Exception as error:

            print("Error al seleccionar el cliente", error)

    def cargar_linea_venta(self, index):

        try:

            tab_ventas = self.ui.tabVentas
            tab_ventas.setRowCount(index)

            for i in range(index):

                self.__crear_row_venta(i)

        except Exception as error:

            print("Error al cargar la línea de ventas", error)

    def __crear_row_venta(self, i):

        try:

            lista_conceptos = conexion.Conexion.cargar_lista_conceptos()
            lista_conceptos.insert(0, "")
            tab_ventas = self.ui.tabVentas

            cmb_servicio = QtWidgets.QComboBox()
            txt_unidades = QtWidgets.QLineEdit()
            btn_borrar = QtWidgets.QPushButton("Retirar")

            btn_borrar.clicked.connect(lambda index: self.__borrar_linea(i))

            txt_unidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            tab_ventas.setCellWidget(i, 0, cmb_servicio)
            tab_ventas.setItem(i, 2, QtWidgets.QTableWidgetItem(str("")))
            tab_ventas.setCellWidget(i, 4, btn_borrar)

            cmb_servicio.addItems(lista_conceptos)
            cmb_servicio.currentIndexChanged.connect(self.__recargar_precios_servicios)

            tab_ventas.setItem(i, 1, QtWidgets.QTableWidgetItem())
            tab_ventas.setItem(i, 3, QtWidgets.QTableWidgetItem())

            tab_ventas.item(i, 1).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
            tab_ventas.item(i, 3).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

            self.conceptos.append(cmb_servicio)

        except Exception as error:

            print("Error al crear una nueva linea de venta", error)

    def __borrar_linea(self, index):

        try:

            if len(self.conceptos) != 1:

                tab_venta = self.ui.tabVentas

                self.conceptos.pop(index)

                print(len(self.conceptos))

            self.__recargar_precios_servicios()

        except Exception as error:

            print("Error al borrar una línea de venta", error)

    def ampliar_linea_ventas(self):

        try:

            if self.conceptos[len(self.conceptos) - 1].currentText() != "":

                tab_ventas = self.ui.tabVentas
                tab_ventas.setRowCount(tab_ventas.rowCount() + 1)

                self.__crear_row_venta(tab_ventas.rowCount() - 1)

        except Exception as error:

            print("Error al ampliar la linea de ventas", error)

    def __cargar_conceptos(self):

        try:

            lista_conceptos = conexion.Conexion.cargar_lista_conceptos()
            lista_conceptos.insert(0, "")

            for cmb in self.conceptos:

                text = cmb.currentText()

                cmb.clear()
                cmb.addItems(lista_conceptos)
                cmb.setCurrentText(text)

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

                    tab_ventas.setItem(i, 1, QtWidgets.QTableWidgetItem(str(precio) + "€"))
                    tab_ventas.setItem(i, 2, QtWidgets.QTableWidgetItem(str("1")))
                    tab_ventas.setItem(i, 3, QtWidgets.QTableWidgetItem(str(precio) + "€"))

                    tab_ventas.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tab_ventas.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tab_ventas.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    precio_total += float(precio.replace(",", "."))

                    # Ampliar para poder incluír más productos
                    self.ampliar_linea_ventas()

            self.ui.lblPrecioTotal.setText(str(precio_total).replace(".", ",") + "€")

        except Exception as error:

            print("Error al cargar el precio del servicio", error)

    def limpiar_facturas(self):

        try:

            self.conceptos.clear()
            self.cargar_linea_venta()
            self.__recargar_precios_servicios()

        except Exception as error:

            print("Error al limpiar la factura", error)