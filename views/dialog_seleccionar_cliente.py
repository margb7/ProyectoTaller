from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QHeaderView, QTableWidget, QTableWidgetItem

import conexion
from dialogs.dlgSeleccionarFactura import Ui_dlgSeleccionCliente


class DialogSeleccionarCliente(QDialog):

    def __init__(self):
        super(DialogSeleccionarCliente, self).__init__()

        self.ui = Ui_dlgSeleccionCliente()
        self.ui.setupUi(self)
        self.ui.btnAceptar.clicked.connect(self.seleccionar_factura)
        self.cliente = None

        self.ui.txtBusqueda.textEdited.connect(self.actualizar_lista_facturas)

        tab_header = self.ui.tabClientes.horizontalHeader()
        tab_header.setSectionResizeMode(QHeaderView.sectionResizeMode(tab_header, 0).Stretch)

        self.ui.tabClientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


        self.actualizar_lista_facturas()

    def actualizar_lista_facturas(self):

        try:

            coches = conexion.Conexion.cargar_lista_coches()
            tab_clientes = self.ui.tabClientes

            tab_clientes.setRowCount(len(coches))

            for i, coche in enumerate(coches):

                item = QTableWidgetItem(str(coche.dnicli))
                item_matr = QTableWidgetItem(str(coche.matricula))

                item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item_matr.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

                tab_clientes.setItem(i, 0, item)
                tab_clientes.setItem(i, 1, item_matr)

        except Exception as error:

            print("Error al actualizar la lista de clientes en dialogo de selección", error)

    def seleccionar_factura(self):

        if len(self.ui.tabClientes.selectedItems()) != 0:

            self.cliente = self.ui.tabClientes.selectedItems()[0].text()

        else:

            self.cliente = None

        self.hide()
