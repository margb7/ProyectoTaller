from ventMain import Ui_mainWindow

from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor


def validar_dni(dni: str) -> bool:
    out = False

    try:

        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        dig_ext = "XYZ"
        reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
        numeros = "1234567890"
        dni = dni.upper()

        if len(dni) == 9:

            dig_control = dni[8]
            dni = dni[:8]

            if dni[0] in dig_ext:
                dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])

            out = len(dni) == len([n for n in dni if n in numeros]) \
                  and tabla[int(dni) % 23] == dig_control

    except Exception as error:

        print("Error al validar el DNI", error)

    return out


def resaltar_campos_obligatorios(ui: Ui_mainWindow):
    ui.txtDNI.setStyleSheet("background-color: yellow")
    ui.txtVehiculo.setStyleSheet("background-color: yellow")
    ui.lblAvisoPago.setVisible(True)


def reset_campos_obligatorios(ui: Ui_mainWindow):
    ui.txtDNI.setStyleSheet("background-color: white")
    ui.txtVehiculo.setStyleSheet("background-color: white")
    ui.lblAvisoPago.setVisible(False)


def fuente_a_pixeles(texto: str, size: int) -> float:
    return len(texto) * size / 12 * 16


def calcular_inicio_texto_centrado(centro: float, texto: str, size: int) -> float:
    return centro - (fuente_a_pixeles(texto, size) / 2)


def resize_tab_bar(ui: Ui_mainWindow):
    try:

        header = ui.tabClientes.horizontalHeader()

        for i in range(5):

            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

            if i == 0 or i == 1:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    except Exception as error:

        print("Error al redimensionar la tabla de coches", error)


def aplicar_colores_tabla(tabla: QtWidgets.QTableWidget):
    try:

        for i in range(0, tabla.columnCount()):

            for j in range(tabla.rowCount()):

                if j % 2 == 0:

                    tabla.item(j, i).setBackground(QColor("#BCBAB8"))

                else:

                    tabla.item(j, i).setBackground(QColor("#F9F9F9"))

    except Exception as error:

        print("Error al aplicar estilo a la tabla", error)


def formatear_ui(ui: Ui_mainWindow):
    ui.txtDireccion.setText(ui.txtDireccion.text().title())
    ui.txtNombreCli.setText(ui.txtNombreCli.text().title())
    ui.txtMarca.setText(ui.txtMarca.text().upper())
    ui.txtModelo.setText(ui.txtModelo.text().capitalize())
    ui.txtVehiculo.setText(ui.txtVehiculo.text().upper())
