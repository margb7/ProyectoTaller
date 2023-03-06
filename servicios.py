import conexion
import events
import ajustes_ui

from PyQt6 import QtWidgets, QtCore, QtGui
from models.models import Servicio
from ventMain import Ui_mainWindow


class TabServicios:

    def __init__(self, ui: Ui_mainWindow):

        self.ui = ui

        # Apartado de servicios

        header = self.ui.tabServicio.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(header, 0).Stretch)

        servicios_header = self.ui.tabClientes.horizontalHeader()
        servicios_header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(servicios_header, 0).Stretch)

        self.ui.txtBuscarConcepto.textChanged.connect(self.buscar_servicio)

        self.ui.btnGuardarServ.clicked.connect(self.guardar_servicio)
        self.ui.btnLimpiarServ.clicked.connect(self.limpiar_ui_servicio)
        self.ui.btnModificarServ.clicked.connect(self.modificar_servicio)
        self.ui.btnEliminarServ.clicked.connect(self.eliminar_servicio)
        self.ui.btnRecargarTabla.clicked.connect(self.cargar_tabla_servicios)

        self.ui.tabServicio.clicked.connect(self.cargar_servicio_desde_tabla)

        self.cargar_tabla_servicios()

    def buscar_servicio(self):
        """
        Busca los servicios a partir del texto de búsqueda
        :return: None
        """

        try:

            nombre = self.ui.txtBuscarConcepto.text()

            if nombre == "":

                self.cargar_tabla_servicios()
                return

            lista_servicios = conexion.Conexion.buscar_servicios_concepto(nombre)

            self.__mostrar_lista_en_tabla(lista_servicios)

        except Exception as error:

            print("Error al buscar un servicio por concepto", error)

    def cargar_tabla_servicios(self):
        """
        Carga la tabla de servicios
        :return: None
        """

        try:

            self.ui.tabServicio.setRowCount(0)
            self.ui.txtBuscarConcepto.setText("")
            lista_servicios = conexion.Conexion.cargar_lista_servicios()

            self.__mostrar_lista_en_tabla(lista_servicios)

        except Exception as error:

            print("Error al cargar la tabla de servicios", error)

    def __mostrar_lista_en_tabla(self, lista):
        """
        Muestra los servicios en la tabla de servicios
        :param lista: la lista de servicios a mostrar
        :return: None
        """

        try:

            i = 0

            self.ui.tabServicio.setRowCount(len(lista) + 1)

            for servicio in lista:
                self.ui.tabServicio.setItem(i, 0, QtWidgets.QTableWidgetItem(str(servicio.codigo)))
                self.ui.tabServicio.setItem(i, 1, QtWidgets.QTableWidgetItem(servicio.concepto))
                self.ui.tabServicio.setItem(i, 2, QtWidgets.QTableWidgetItem(str(servicio.precio_unidad)))

                item0 = self.ui.tabServicio.item(i, 0)
                item1 = self.ui.tabServicio.item(i, 1)
                item2 = self.ui.tabServicio.item(i, 2)

                item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                item0.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item1.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item2.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

                i += 1

            ultima_fila = self.ui.tabServicio.rowCount() - 1

            for i in range(5):
                item = QtWidgets.QTableWidgetItem("")
                item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

                self.ui.tabServicio.setItem(ultima_fila, i, item)

            self.ui.tabServicio.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)

            ajustes_ui.aplicar_colores_tabla(self.ui.tabServicio)

        except Exception as error:

            print("Error al mostrar lista en tabla", error)

    def cargar_servicio_desde_tabla(self):
        """
        Carga un servicio seleccionado en la tabla de servicios
        :return: None
        """

        try:

            num_fila = self.ui.tabServicio.currentRow()

            datos = [self.ui.txtCodigo, self.ui.txtConceptoServicio, self.ui.txtPrecioUnidad]

            for i in range(self.ui.tabServicio.columnCount()):

                if self.ui.tabServicio.item(num_fila, i) is not None:

                    valor = self.ui.tabServicio.item(num_fila, i).text()

                    datos[i].setText(valor)

        except Exception as error:

            print("Error al cargar un servicio desde la tabla", error)

    def modificar_servicio(self):
        """
        Modifica un servicio
        :return: None
        """

        try:

            if self.ui.txtCodigo.text() == "Auto-generado":

                events.Eventos.lanzar_error("Primero crea un servicio o carga uno desde la tabla")

            else:

                servicio = self.cargar_servicio_ui()

                if conexion.Conexion.modifica_servicio(servicio):

                    events.Eventos.lanzar_aviso("Se ha modificado correctamente")

                    self.cargar_tabla_servicios()
                    self.limpiar_ui_servicio()

                else:

                    events.Eventos.lanzar_error("No se ha podido modificar")

        except Exception as error:

            print("Error al modificar un servicio", error)

    def eliminar_servicio(self):
        """
        Elimina un servicio
        :return: None
        """

        try:

            if self.ui.txtCodigo.text() == "Auto-generado":

                events.Eventos.lanzar_error("Primero crea un servicio o cárgalo desde la tabla")

            else:

                if conexion.Conexion.borraServicioPorCodigo(self.ui.txtCodigo.text()):

                    events.Eventos.lanzar_aviso("Servicio borrado correctamente")

                    self.cargar_tabla_servicios()
                    self.limpiar_ui_servicio()

                else:

                    events.Eventos.lanzar_error("No se pudo borrar el servicio")

        except Exception as error:

            print("Error al eliminar un servicio", error)

    def guardar_servicio(self):
        """
        Guarda un sercvicio en la base de datos a partir de los datos de la interfaz
        :return: None
        """

        try:

            precio_unidad = self.ui.txtPrecioUnidad.text()
            concepto = self.ui.txtConceptoServicio.text()

            if precio_unidad == "":

                events.Eventos.lanzar_error("El precio por unidad no puede estar vacío")

            elif concepto == "":

                events.Eventos.lanzar_error("El concepto no puede estar vacío")

            else:

                servicio = self.cargar_servicio_ui()

                if servicio is None:

                    events.Eventos.lanzar_error("No se pudo guardar el cliente")

                else:

                    if conexion.Conexion.guardar_servicio(servicio):

                        events.Eventos.lanzar_aviso("Se ha guardado el servicio")
                        self.cargar_tabla_servicios()
                        self.limpiar_ui_servicio()

                    else:

                        events.Eventos.lanzar_error("No se ha podido guardar el servicio")

        except Exception as error:

            print("Error al guardar el servicio", error)

    def limpiar_ui_servicio(self):
        """
        Limpia la interfaz de servicios
        :return: None
        """

        try:

            self.ui.txtConceptoServicio.setText("")
            self.ui.txtPrecioUnidad.setText("")
            self.ui.txtCodigo.setText("Auto-generado")

        except Exception as error:

            print("Error al limpiar la UI de servicios", error)

    def cargar_servicio_ui(self) -> Servicio:
        """
        Carga un servicio a partir de los datos de la interfaz
        :return: el servicio cargado o None si no se pudo cargar
        """

        servicio = None

        try:

            concepto = self.ui.txtConceptoServicio.text()
            precio_unidad = self.ui.txtPrecioUnidad.text()
            codigo = -1

            if self.ui.txtCodigo.text() != "Auto-generado":

                codigo = self.ui.txtCodigo.text()

            servicio = Servicio(concepto, precio_unidad, codigo)

        except Exception as error:

            print("Error al cargar un servicio desde la UI", error)

        return servicio

    def mostrar_servicio_ui(self, servicio: Servicio):
        """
        Muestra un servicio en la interfaz
        :param servicio: el servicio a mostrar
        :return: None
        """

        try:

            self.ui.txtCodigo.setText(str(servicio.codigo))
            self.ui.txtConceptoServicio.setText(servicio.concepto)
            self.ui.txtPrecioUnidad.setText(servicio.precio_unidad)

        except Exception as error:

            print("Error al mostrar servicio", error)
