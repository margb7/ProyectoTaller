import typing

import conexion
import events
import views.dialog_seleccionar_cliente
from bbdd.facturas_dao import FacturaDAO
from bbdd.servicios_dao import ServicioDAO

from models.factura import Factura
from models.informe import Informe

from ventMain import Ui_mainWindow
from PyQt6 import QtCore, QtSql
from PyQt6.QtWidgets import QComboBox, QHeaderView, QTableWidget, QLineEdit, QPushButton, QTableWidgetItem, QSpinBox


class TabFacturacion:

    def __init__(self, ui: Ui_mainWindow):

        self.ui = ui
        self.conceptos: typing.List[QComboBox] = []
        self.unidades: typing.List[QSpinBox] = []

        self.dlg_seleccionar_cliente = views.dialog_seleccionar_cliente.DialogSeleccionarCliente()
        self.cliente = None
        self.factura = None

        facturacion_header = self.ui.tabFacturas.horizontalHeader()
        facturacion_header.setSectionResizeMode(QHeaderView.sectionResizeMode(facturacion_header, 0).Stretch)

        self.ui.tabVentas.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.ui.tabVentas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.ui.tabFacturas.itemSelectionChanged.connect(self.__cargar_factura_desde_tab)

        ventas_header = self.ui.tabVentas.horizontalHeader()
        ventas_header.setSectionResizeMode(QHeaderView.sectionResizeMode(ventas_header, 0).Stretch)

        ventas_header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        # Cargar conceptos a medida que se crean o destruyen
        self.ui.btnGuardarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnEliminarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnModificarServ.clicked.connect(self.__cargar_conceptos)
        self.ui.btnSeleccionarCliente.clicked.connect(self.dlg_seleccionar_cliente.show)
        self.ui.btnImprimirFactura.clicked.connect(self.imprimir_factura)

        self.dlg_seleccionar_cliente.ui.btnAceptar.clicked.connect(self.seleccionar_cliente)
        self.ui.btnLimpiarFact.clicked.connect(self.limpiar_facturas)
        self.ui.btnProcesarFact.clicked.connect(self.crear_factura)

        self.cargar_linea_venta(1)
        self.__actualizar_lista_facturas()

    def __cargar_factura_desde_tab(self):

        try:

            if len(self.ui.tabFacturas.selectedItems()) == 0:
                return

            row = self.ui.tabFacturas.selectedItems()[0].row()
            idfact = int(self.ui.tabFacturas.item(row, 1).text())

            factura = FacturaDAO.obtener_factura_por_id(idfact)

            if factura is not None:

                self.factura = factura

                self.conceptos.clear()
                self.unidades.clear()

                self.ui.txtNumFactura.setText(str(factura.id_factura))
                self.ui.txtFactDni.setText(str(factura.dni))
                self.ui.txtMatriculaFact.setText(str(factura.matricula))

                ventas = FacturaDAO.cargar_servicios_de_factura(factura.id_factura)

                self.ui.tabVentas.setRowCount(len(ventas) + 1)

                for i, vent in enumerate(ventas):

                    self.__crear_row_venta(i, vent.concepto, vent.unidades, vent.precio_unidad)

                self.__crear_row_venta(len(ventas))
                self.__recargar_precios_servicios()

        except Exception as error:

            print("Error al cargar la factura desde la tabla de facturas", error)

    def __actualizar_lista_facturas(self):

        try:

            facturas = FacturaDAO.obtener_facturas()

            self.ui.tabFacturas.setRowCount(len(facturas))

            for i, fact in enumerate(facturas):

                dni_item = QTableWidgetItem(str(fact.dni))
                id_item = QTableWidgetItem(str(fact.id_factura))

                dni_item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                id_item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

                self.ui.tabFacturas.setItem(i, 0, dni_item)
                self.ui.tabFacturas.setItem(i, 1, id_item)

        except Exception as error:

            print("Error al actualizar la lista de facturas", error)

    def imprimir_factura(self):

        try:

            num_factura = self.ui.txtNumFactura.text()

            factura: Factura

            if num_factura == "":

                factura = Factura(1, self.ui.txtFactDni.text(), self.ui.txtMatriculaFact.text(), "Fecha tempp")

            conceptos_str = []
            lista_unidades = []
            lista_precios = []

            for i, c in enumerate(self.conceptos):

                if c.currentText() != "":

                    nuevo_concepto = c.currentText()

                    servicio = ServicioDAO.cargar_servicio_por_concepto(nuevo_concepto)

                    precio_unidad = servicio.precio_unidad
                    unidades = self.unidades[i].value()

                    conceptos_str.append(nuevo_concepto)
                    lista_precios.append(precio_unidad)
                    lista_unidades.append(int(unidades))

            Informe.generar_informe_factura(factura, conceptos_str, lista_unidades, lista_precios)

        except Exception as error:

            print("Error al imprimir factura", error)

    def seleccionar_cliente(self):

        try:

            cliente_coche = self.dlg_seleccionar_cliente.cliente
            cliente = conexion.Conexion.one_cli(cliente_coche.dnicli)

            if cliente is not None:

                self.ui.txtFactDni.setText(cliente.dni)
                self.ui.txtProvinciaFact.setText(cliente.provincia)
                self.ui.txtMatriculaFact.setText(cliente_coche.matricula)

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

    def __crear_row_venta(self, i, concepto: str = "", num_unidades: int = 1, precio_unidad: float = -1):

        try:

            lista_conceptos = conexion.Conexion.cargar_lista_conceptos()
            lista_conceptos.insert(0, "")
            tab_ventas = self.ui.tabVentas

            cmb_servicio = QComboBox()
            spn_unidades = QSpinBox()

            spn_unidades.setValue(num_unidades)
            spn_unidades.setMinimum(1)

            cmb_servicio.addItems(lista_conceptos)
            cmb_servicio.setCurrentText(concepto)
            cmb_servicio.currentIndexChanged.connect(self.__recargar_precios_servicios)

            btn_borrar = QPushButton("Retirar")

            btn_borrar.clicked.connect(lambda index: self.__borrar_linea(i))

            tab_ventas.setCellWidget(i, 0, cmb_servicio)
            tab_ventas.setCellWidget(i, 2, spn_unidades)
            tab_ventas.setCellWidget(i, 4, btn_borrar)

            spn_unidades.valueChanged.connect(self.__recargar_precios_servicios)

            if precio_unidad != -1:

                tab_ventas.setItem(i, 1, QTableWidgetItem(str("{:.2f}".format(precio_unidad) + "€")))

            else:

                tab_ventas.setItem(i, 1, QTableWidgetItem(""))

            tab_ventas.setItem(i, 3, QTableWidgetItem())

            tab_ventas.item(i, 1).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
            tab_ventas.item(i, 3).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

            self.conceptos.append(cmb_servicio)
            self.unidades.append(spn_unidades)

        except Exception as error:

            print("Error al crear una nueva linea de venta", error)

    def __borrar_linea(self, index):

        try:

            if len(self.conceptos) != 1:

                tab_venta = self.ui.tabVentas
                self.conceptos.pop(index)
                self.unidades.pop(index)
                tab_venta.removeRow(index)

            self.__recargar_precios_servicios()

        except Exception as error:

            print("Error al borrar una línea de venta", error)
            print("Index: " + index)

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

                    tab_ventas.setItem(i, 1, QTableWidgetItem(str("")))
                    tab_ventas.setItem(i, 1, QTableWidgetItem(str("")))
                    tab_ventas.setItem(i, 3, QTableWidgetItem(str("")))

                else:

                    preciostr = self.ui.tabVentas.item(i, 1).text()

                    if preciostr != "":

                        preciostr = self.ui.tabVentas.item(i, 1).text().replace("€", "")

                    else:

                        preciostr = conexion.Conexion.obtener_precio_servicio_por_concepto(cmb.currentText())

                    preciostr = preciostr.replace(",", ".")

                    precio = float(preciostr)

                    tab_ventas.setItem(i, 1, QTableWidgetItem(str("{:.2f}".format(precio)) + "€"))

                    subtotal = precio * self.unidades[i].value()

                    tab_ventas.setItem(i, 3, QTableWidgetItem("{:.2f}".format(subtotal) + "€"))

                    tab_ventas.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tab_ventas.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    precio_total += float(subtotal)

                    # Ampliar para poder incluír más productos
                    self.ampliar_linea_ventas()

            self.ui.lblPrecioTotal.setText(str("{:.2f}".format(precio_total)).replace(".", ",") + "€")

        except Exception as error:

            print("Error al cargar el precio del servicio", error)

    def limpiar_facturas(self):

        try:

            self.cliente = None
            self.factura = None

            self.conceptos.clear()
            self.unidades.clear()
            self.cargar_linea_venta(1)
            self.__recargar_precios_servicios()
            self.ui.txtFactDni.setText("")
            self.ui.txtMatriculaFact.setText("")
            self.ui.txtNumFactura.setText("")
            self.ui.txtProvinciaFact.setText("")

        except Exception as error:

            print("Error al limpiar la factura", error)

    def crear_factura(self):

        try:

            dni = self.ui.txtFactDni.text()
            matricula = self.ui.txtMatriculaFact.text()

            if dni == "" or matricula == "":

                events.Eventos.lanzar_error("Selecciona una factura primero")
                return

            idfact = FacturaDAO.crear_factura(dni, matricula)

            if idfact != -1:

                for i, conc in enumerate(self.conceptos):

                    text = conc.currentText()

                    if text != "":

                        unidades = self.unidades[i].value()
                        servicio = ServicioDAO.cargar_servicio_por_concepto(text)

                        if servicio is not None:

                            FacturaDAO.guardar_venta_factura(idfact, int(servicio.codigo), unidades)

                events.Eventos.lanzar_aviso("Factura registrada")
                self.__actualizar_lista_facturas()

            else:

                events.Eventos.lanzar_error("Error al registrar factura")

        except Exception as error:

            print("Error al crear una factura", error)