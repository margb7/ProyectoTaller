import sys

from datetime import datetime
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate

from ventCalendario import Ui_ventCalendar
from dlgSalir import Ui_Dialog
from dlgExportarDatos import Ui_dlgExportarDatos


class FileDialogAbrir(QtWidgets.QFileDialog):

    def __init__(self):
        super(FileDialogAbrir, self).__init__()


class DialogSalir(QtWidgets.QDialog):

    def __init__(self):
        super(DialogSalir, self).__init__()
        self.aviso_salir = Ui_Dialog()
        self.aviso_salir.setupUi(self)

        self.aviso_salir.btnSalir.clicked.connect(DialogSalir.__salir)
        self.aviso_salir.pushButton_2.clicked.connect(self.hide)

    @staticmethod
    def __salir():

        sys.exit(0)


class VentCalendario(QtWidgets.QMainWindow):

    def __init__(self):
        super(VentCalendario, self).__init__()
        self.ui = Ui_ventCalendar()
        self.ui.setupUi(self)

        self.date = QDate()

        dia = datetime.now().day
        mes = datetime.now().month
        year = datetime.now().year

        self.ui.calendarWidget.setSelectedDate((QtCore.QDate(year, mes, dia)))
        self.ui.calendarWidget.clicked.connect(self.guardar_fecha)

    def guardar_fecha(self, date):

        self.date = date
        self.hide()


class DialogExportarDatos(QtWidgets.QDialog):

    def __init__(self):
        super(DialogExportarDatos, self).__init__()
        self.ui = Ui_dlgExportarDatos()
        self.ui.setupUi(self)
