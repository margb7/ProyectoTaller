import typing

from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QHeaderView, QTableWidget, QTableWidgetItem

from dialogs.dlgSeleccionarFactura import Ui_dlgSeleccionCliente
from bbdd.coches_dao import CochesDAO
from models.models import Coche


class DialogSeleccionarCliente(QDialog):

    def __init__(self):
        super(DialogSeleccionarCliente, self).__init__()

        self.ui = Ui_dlgSeleccionCliente()
        self.ui.setupUi(self)
        self.cliente: Coche = None
        self.coches = []

        tab_header = self.ui.tabClientes.horizontalHeader()
        tab_header.setSectionResizeMode(QHeaderView.sectionResizeMode(tab_header, 0).Stretch)

        self.ui.txtBusqueda.textEdited.connect(self.actualizar_lista_facturas)

        self.ui.btnAceptar.clicked.connect(self.seleccionar_factura)
        self.ui.btnCancelar.clicked.connect(self.hide)

        self.ui.tabClientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.actualizar_lista_facturas()

    def actualizar_lista_facturas(self):

        try:

            search_str = self.ui.txtBusqueda.text()

            self.coches = CochesDAO.buscarPorDni(search_str)

            tab_clientes = self.ui.tabClientes
            tab_clientes.setRowCount(len(self.coches))

            for i, coche in enumerate(self.coches):

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

            index = self.ui.tabClientes.selectedItems()[0].row().__index__()

            self.cliente = self.coches[index]

        else:

            self.cliente = None

        self.hide()
