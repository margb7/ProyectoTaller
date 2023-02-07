from PyQt6 import QtWidgets, QtCore

import conexion
from dialogs.dlgSeleccionarCliente import Ui_dlgSeleccionCliente


class DialogSeleccionarCliente(QtWidgets.QDialog):

    def __init__(self):
        super(DialogSeleccionarCliente, self).__init__()

        self.ui = Ui_dlgSeleccionCliente()
        self.ui.setupUi(self)
        self.ui.btnAceptarCliente.clicked.connect(self.seleccionar_cliente)
        self.cliente = None

        tab_header = self.ui.tabClientes.horizontalHeader()
        tab_header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(tab_header, 0).Stretch)

        self.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)

        self.actualizar_lista_clientes()

    def actualizar_lista_clientes(self):

        try:

            coches = conexion.Conexion.cargar_lista_coches()
            tab_clientes = self.ui.tabClientes

            tab_clientes.clear()
            tab_clientes.setRowCount(len(coches))

            for i, coche in enumerate(coches):

                item = QtWidgets.QTableWidgetItem(str(coche.dnicli))
                item_matr = QtWidgets.QTableWidgetItem(str(coche.matricula))

                item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item_matr.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

                tab_clientes.setItem(i, 0, item)
                tab_clientes.setItem(i, 1, item_matr)

        except Exception as error:

            print("Error al actualizar la lista de clientes en dialogo de selección", error)

    def seleccionar_cliente(self):

        if len(self.ui.tabClientes.selectedItems()) != 0:

            self.cliente = self.ui.tabClientes.selectedItems()[0].text()

        else:

            self.cliente = None

        self.hide()
