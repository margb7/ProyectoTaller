import sys

import conexion
from views import views

from PyQt6 import QtWidgets, QtCore, QtGui

import ajustes_ui
import events
from models.models import Coche, Cliente
from ventMain import Ui_mainWindow


class Main(QtWidgets.QMainWindow):

    def __init__(self):

        # Setup UI
        super(Main, self).__init__()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.objSalir = views.DialogSalir()
        self.objCalendar = views.VentCalendario()
        self.dlgExportarDatos = views.DialogExportarDatos()

        # Texto barra de estado

        self.lblTiempo = QtWidgets.QLabel("")

        self.contador = QtCore.QTimer(self)

        self.contador.setInterval(1000)
        self.contador.timeout.connect(self._actualizar_tiempo)

        self.contador.start()

        self.ui.statusbar.addWidget(self.lblTiempo)
        self.ui.statusbar.addPermanentWidget(QtWidgets.QLabel("Mario González Besada - 2DAM"))

        # Events
        self.ui.actionSalir.triggered.connect(self.salir)
        self.ui.actionSalirbar.triggered.connect(self.salir)
        self.ui.btnSalir.clicked.connect(self.salir)

        self.ui.actionGuardar_Copia_Seguridad.triggered.connect(events.Eventos.crea_backup)
        self.ui.actionRestaurar_Copia_Seguridad.triggered.connect(self.restaurar_backup)

        self.ui.actionExportar_Datos.triggered.connect(self.dlg_exportar_datos)
        self.ui.actionImportar_Datos.triggered.connect(self.importar_desde_excel)

        self.ui.txtDNI.editingFinished.connect(self.mostrar_dni_valido)

        self.ui.txtDireccion.editingFinished.connect(lambda: ajustes_ui.formatear_ui(self.ui))
        self.ui.txtMarca.editingFinished.connect(lambda: ajustes_ui.formatear_ui(self.ui))
        self.ui.txtModelo.editingFinished.connect(lambda: ajustes_ui.formatear_ui(self.ui))
        self.ui.txtVehiculo.editingFinished.connect(lambda: ajustes_ui.formatear_ui(self.ui))
        self.ui.txtNombreCli.editingFinished.connect(lambda: ajustes_ui.formatear_ui(self.ui))

        self.ui.btnLimpiar.clicked.connect(self.limpiar_ui)

        self.ui.pushButton_2.clicked.connect(self.mostrar_coches)
        self.ui.btnGuardaCli.clicked.connect(self.guarda_cliente)  # Botón para guardar cliente
        self.ui.btnBorraCli.clicked.connect(self.borrar_cliente)  # Botón para borrar cliente
        self.ui.btnFechaAltaCli.clicked.connect(self.carga_fecha)

        self.ui.tabClientes.clicked.connect(self.carga_cliente_desde_tab)
        self.ui.btnModifCli.clicked.connect(self.modificar_cliente)

        header = self.ui.tabClientes.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.sectionResizeMode(header, 0).Stretch)

        self.mostrar_provincias()
        self.mostrar_coches()

        self.ui.cmbProcli.currentIndexChanged.connect(self.mostrar_municipios)

        self.ui.lblAvisoPago.setVisible(False)

        self._aplicar_estilos()

    def _actualizar_tiempo(self):

        try:

            texto = QtCore.QTime.currentTime().toString()[:-3]

            texto += " - " + QtCore.QDate.currentDate().toString()

            self.lblTiempo.setText(texto)

        except Exception:

            pass

    def _aplicar_estilos(self):

        css = "./css/label_bold.css"
        with open(css, "r") as file:

            elementos = [
                self.ui.lblDNI
            ]

            file = file.read()

            for el in elementos:

                el.setStyleSheet(file)

    def modificar_cliente(self):

        try:

            if self.ui.txtDNI.text() == "":

                events.Eventos.lanzar_error("Selecciona un cliente primero")

            else:

                conexion.Conexion.modifica_cli(self.cargar_cliente_ui(), self.cargar_coche_ui())
                self.mostrar_coches()

        except Exception as error:

            print("Error al modificar cliente desde UI", error)

    def sel_motor(self) -> str:

        motor = ""

        try:

            if self.ui.rbtGasolina.isChecked():

                motor = "Gasolina"

            elif self.ui.rbtDiesel.isChecked():

                motor = "Diesel"

            elif self.ui.rbtHibrido.isChecked():

                motor = "Híbrido"

            elif self.ui.rbtElectrico.isChecked():

                motor = "Eléctrico"

        except Exception as error:

            print("Error al seleccionar el motor: ", error)

        return motor

    def cargar_coche_ui(self) -> Coche:

        try:

            coche = Coche(matricula=self.ui.txtVehiculo.text(), modelo=self.ui.txtModelo.text(),
                          dnicli=self.ui.txtDNI.text(),
                          motor=self.sel_motor(), marca=self.ui.txtMarca.text())

        except Exception as error:

            print("Error al cargar coche desde UI", error)

            coche = None

        return coche

    def cargar_cliente_ui(self) -> Cliente:

        try:

            pagos = []

            if self.ui.chkTarj.isChecked():

                pagos.append("Tarjeta")

            if self.ui.chkEfec.isChecked():

                pagos.append("Efectivo")

            if self.ui.chkTrans.isChecked():

                pagos.append("Transferencia")

            pagos = set(pagos)
            pagos = '; '.join(pagos)

            out = Cliente(self.ui.txtDNI.text(), self.ui.txtNombreCli.text(), self.ui.txtFechaAlta.text(),
                          self.ui.txtDireccion.text(), self.ui.cmbProcli.currentText(),
                          self.ui.cmbMunicli.currentText(), pagos)

        except Exception as error:

            print("Error al cargar el cliente desde UI", error)

            out = None

        return out

    def mostrar_dni_valido(self):

        try:

            dni = self.ui.txtDNI.text()

            if ajustes_ui.validar_dni(dni):

                self.ui.txtDNI.setStyleSheet("color: green")
                self.ui.txtDNI.setText(dni.upper())

            else:

                self.ui.txtDNI.setStyleSheet("color: red")

        except Exception as error:

            print("Error al mostrar el marcado de validez del DNI", error)

    def carga_fecha(self):

        try:

            self.objCalendar.ui.calendarWidget.clicked.connect(self.mostrar_fecha)
            self.objCalendar.show()

        except Exception as error:

            print("Error al cargar la fecha ", error)

    def mostrar_fecha(self, date):

        try:

            date = '{0}/{1}/{2}'.format(date.day(), date.month(), date.year())

            self.ui.txtFechaAlta.setText(date)
            self.objCalendar.hide()

        except Exception as error:

            print("Error al mostrar la fecha", error)

    def borrar_cliente(self):

        borrado = False

        try:

            matricula = self.ui.txtVehiculo.text()
            dni = self.ui.txtDNI.text()

            if self.ui.txtDNI.text() == "":

                events.Eventos.lanzar_error("Selecciona un cliente primero")

            else:

                if conexion.Conexion.borraCochePorMatricula(matricula):
                    borrado = conexion.Conexion.borraCliPorDni(dni)

                if borrado:

                    msg = QtWidgets.QMessageBox()
                    msg.setModal(True)
                    msg.setWindowTitle("Aviso")
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText("Cliente dado de baja")
                    msg.exec()

                else:

                    events.Eventos.lanzar_error("No se pudo dar de baja al cliente")

                self.limpiar_ui()
                self.mostrar_coches()

        except Exception as error:

            print("Error al intentar borrar un cliente", error)

    def mostrar_municipios(self):

        try:

            self.ui.cmbMunicli.clear()
            self.ui.cmbMunicli.addItem('')

            lista_municipios = conexion.Conexion.cargar_municipios(self.ui.cmbProcli.currentText())

            for muni in lista_municipios:
                self.ui.cmbMunicli.addItem(muni)

        except Exception as error:

            print("Error al cargar municipios de UI", error)

    def mostrar_provincias(self):

        try:

            self.ui.cmbProcli.clear()
            self.ui.cmbProcli.addItem("")

            lista_provincias = conexion.Conexion.cargar_provincias()

            for provincia in lista_provincias:
                self.ui.cmbProcli.addItem(provincia)

        except Exception as error:

            print("Error al cargar las provincias", error)

    def mostrar_coches(self):

        try:

            self.ui.tabClientes.setRowCount(0)

            i = 0
            lista_coches = conexion.Conexion.cargar_lista_coches()

            self.ui.tabClientes.setRowCount(len(lista_coches) + 1)

            for coche in lista_coches:

                self.ui.tabClientes.setItem(i, 0, QtWidgets.QTableWidgetItem(coche.dnicli))
                self.ui.tabClientes.setItem(i, 1, QtWidgets.QTableWidgetItem(coche.matricula))
                self.ui.tabClientes.setItem(i, 2, QtWidgets.QTableWidgetItem(coche.marca))
                self.ui.tabClientes.setItem(i, 3, QtWidgets.QTableWidgetItem(coche.modelo))
                self.ui.tabClientes.setItem(i, 4, QtWidgets.QTableWidgetItem(coche.motor))

                item0 = self.ui.tabClientes.item(i, 0)
                item1 = self.ui.tabClientes.item(i, 1)
                item2 = self.ui.tabClientes.item(i, 2)
                item3 = self.ui.tabClientes.item(i, 3)

                item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                item0.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item1.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item2.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
                item3.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

                i += 1

            ultima_fila = self.ui.tabClientes.rowCount() - 1

            for i in range(3):

                self.ui.tabClientes.setItem(ultima_fila, i, QtWidgets.QTableWidgetItem(""))

                self.ui.tabClientes.item(ultima_fila, i).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)

            self.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)

        except Exception as error:

            print("Error al mostrar el listado de coches clientes", error)

    def mostrar_cliente(self, cliente: Cliente):

        self.limpiar_ui_cliente()

        self.ui.txtDNI.setText(cliente.dni)
        self.ui.txtNombreCli.setText(cliente.nombre)
        self.ui.txtFechaAlta.setText(cliente.alta)
        self.ui.txtDireccion.setText(cliente.direccion)
        self.ui.cmbProcli.setCurrentText(cliente.provincia)
        self.ui.cmbMunicli.setCurrentText(cliente.municipio)

        self.ui.chkEfec.setChecked('Efectivo' in cliente.pago)
        self.ui.chkTarj.setChecked('Tarjeta' in cliente.pago)
        self.ui.chkTrans.setChecked('Transferencia' in cliente.pago)

    def restaurar_backup(self):

        try:

            events.Eventos.restaurar_backup()
            self.mostrar_coches()

        except Exception as error:

            print("Error al cargar backup desde UI", error)

    def salir(self):
        try:

            self.objSalir.show()

        except Exception as error:

            print("Error al salir ", str(error))

    def carga_cliente_desde_tab(self):

        try:

            num_fila = self.ui.tabClientes.currentRow()
            datos = [self.ui.txtDNI, self.ui.txtVehiculo, self.ui.txtMarca, self.ui.txtModelo]

            for i in range(self.ui.tabClientes.columnCount() - 1):

                if self.ui.tabClientes.item(num_fila, i) is not None:

                    valor = self.ui.tabClientes.item(num_fila, i).text()

                    datos[i].setText(valor)

                i += 1

            if self.ui.tabClientes.item(num_fila, 4) is not None:

                tipo_combustible = self.ui.tabClientes.item(num_fila, 4).text()

                if tipo_combustible == "Diesel":

                    self.ui.rbtDiesel.setChecked(True)

                elif tipo_combustible == "Gasolina":

                    self.ui.rbtGasolina.setChecked(True)

                elif tipo_combustible == "Eléctrico":

                    self.ui.rbtElectrico.setChecked(True)

                else:

                    self.ui.rbtHibrido.setChecked(True)

            dni = self.ui.txtDNI.text()
            registro = conexion.Conexion.one_cli(dni)

            self.limpiar_ui_cliente()

            if registro:

                self.mostrar_cliente(registro)

            else:

                self.ui.txtDNI.setText(dni)

        except Exception as error:

            print("Error al cargar el cliente", error)

    def dlg_exportar_datos(self):

        try:

            self.dlgExportarDatos.ui.btnExportar.clicked.connect(self.exportar_datos_excel)
            self.dlgExportarDatos.show()

        except Exception as error:

            print("Error al lanzar del dialogo para exportar datos", error)

    def exportar_datos_excel(self):

        try:

            self.dlgExportarDatos.hide()

            exportar_clientes = self.dlgExportarDatos.ui.chkClientes.isChecked()
            exportar_coches = self.dlgExportarDatos.ui.chkCoches.isChecked()

            events.Eventos.exportar_datos(exportar_clientes, exportar_coches)

        except Exception as error:

            print("Error al exportar datos a excel", error)

    def importar_desde_excel(self):

        try:

            events.Eventos.importar_datos_excel()
            self.mostrar_coches()

        except Exception as error:

            print("Error al importar datos desde excel", error)

    def guarda_cliente(self):

        try:

            if self.ui.txtDNI.text() == "" or self.ui.txtVehiculo.text() == "":

                events.Eventos.lanzar_error("Completa los campos obligatorios")

                ajustes_ui.resaltar_campos_obligatorios(self.ui)

            elif not ajustes_ui.validar_dni(self.ui.txtDNI.text()):

                events.Eventos.lanzar_error("El DNI debe ser correcto")

            else:

                ajustes_ui.reset_campos_obligatorios(self.ui)

                if conexion.Conexion.alta_cli(self.cargar_cliente_ui(), self.cargar_coche_ui()):

                    events.Eventos.lanzar_aviso("Cliente - coche dado de alta")
                    self.mostrar_coches()
                    self.limpiar_ui()

                else:

                    events.Eventos.lanzar_error("No se pudo dar de alta el cliente y el coche")

        except Exception as error:

            print("Error al guardar el cliente: ", error)

    def limpiar_ui(self):

        try:

            elementos = [self.ui.txtDNI, self.ui.txtModelo, self.ui.txtFechaAlta, self.ui.txtVehiculo, self.ui.txtMarca,
                         self.ui.txtDireccion, self.ui.txtNombreCli]

            for el in elementos:
                el.setText("")

            self.ui.chkEfec.setChecked(False)
            self.ui.chkTarj.setChecked(False)
            self.ui.chkTrans.setChecked(False)

            self.mostrar_provincias()

        except Exception as error:

            print("Error al limpiar: ", error)

    def limpiar_ui_cliente(self):

        try:

            self.ui.cmbMunicli.setCurrentText("")

            elementos = [self.ui.txtDNI, self.ui.txtFechaAlta,
                         self.ui.txtDireccion, self.ui.txtNombreCli]

            for el in elementos:

                el.setText("")

            self.mostrar_provincias()

        except Exception as error:

            print("Error al limpiar UI de cliente", error)


if __name__ == '__main__':
    conexion.Conexion.conexion()

    app = QtWidgets.QApplication([])
    window = Main()

    # Fuentes de texto
    QtGui.QFontDatabase.addApplicationFont("./fonts/Roboto-Regular.ttf")
    QtGui.QFontDatabase.addApplicationFont("./fonts/Roboto-Bold.ttf")

    # Tema para aplicación desde CSS
    archivo_css = "./css/theme.css"
    with open(archivo_css, "r") as f:
        app.setStyleSheet(f.read())

    window.show()
    sys.exit(app.exec())
