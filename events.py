"""
Fichero de eventos
"""
import os
import shutil
import zipfile

import xlrd
import xlwt

import conexion
import ajustes_ui
import views

from datetime import datetime
from models.models import Coche, Cliente, Servicio
from PyQt6 import QtWidgets, QtSql


class Eventos:

    @staticmethod
    def lanzar_error(mensaje_error: str):

        try:

            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle("Error")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setText(mensaje_error)
            msg.exec()

        except Exception as error:

            print("Error al lanzar el mensaje de error", error)

    @staticmethod
    def lanzar_aviso(mensaje_aviso: str):

        try:

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText(mensaje_aviso)
            msg.exec()

        except Exception as error:

            print("Error al lanzar el mensaje de aviso", error)

    @staticmethod
    def exportar_datos(exportar_clientes: bool, exportar_coches: bool, exportar_productos: bool):

        try:

            dlg_abrir = views.views.FileDialogAbrir()

            if exportar_clientes or exportar_coches or exportar_productos:

                fecha = datetime.today()
                nombre = fecha.strftime('%Y_%m_%d_%H-%M-%S_datos.xls')

                directorio, filename = dlg_abrir.getSaveFileName(None, 'Guardar Datos', nombre, '.xls')

                if directorio != '' and filename != '':

                    wb = xlwt.Workbook()

                    if exportar_clientes:

                        sheet1 = wb.add_sheet("Clientes")
                        sheet1.write(0, 0, 'DNI')
                        sheet1.write(0, 1, 'NOMBRE')
                        sheet1.write(0, 2, 'FECHA ALTA')
                        sheet1.write(0, 3, 'DIRECCIÓN')
                        sheet1.write(0, 4, 'PROVINCIA')
                        sheet1.write(0, 5, 'MUNICIPIO')
                        sheet1.write(0, 6, 'FORMA DE PAGO')

                        query = QtSql.QSqlQuery()
                        query.prepare("select * from clientes order by dni")

                        if query.exec():

                            fila = 1

                            while query.next():

                                for i in range(7):
                                    sheet1.write(fila, i, str(query.value(i)))

                                fila += 1

                    if exportar_coches:

                        sheet2 = wb.add_sheet("Coches")
                        sheet2.write(0, 0, "MATRÍCULA")
                        sheet2.write(0, 1, "DNICLI")
                        sheet2.write(0, 2, "MARCA")
                        sheet2.write(0, 3, "MODELO")
                        sheet2.write(0, 4, "MOTOR")

                        query = QtSql.QSqlQuery()
                        query.prepare("select * from coches order by matricula")

                        if query.exec():

                            fila = 1

                            while query.next():

                                for i in range(5):
                                    sheet2.write(fila, i, str(query.value(i)))

                                fila += 1

                    if exportar_productos:

                        sheet3 = wb.add_sheet("Productos")

                        sheet3.write(0, 0, "Código")
                        sheet3.write(0, 1, "Concepto")
                        sheet3.write(0, 2, "Precio_unidad")

                        query = QtSql.QSqlQuery()
                        query.prepare("select * from productos order by codigo")

                        if query.exec():

                            fila = 1

                            while query.next():

                                for i in range(3):

                                    sheet3.write(fila, i, str(query.value(i)))

                                fila += 1

                    wb.save(directorio)

                    Eventos.lanzar_aviso("Datos exportados")

        except Exception as error:

            print("Error al exportar datos", error)

    @staticmethod
    def crea_backup():

        try:

            dlg_abrir = views.views.FileDialogAbrir()

            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H-%M-%S_backup.zip')

            copia = str(fecha)
            directorio, filename = dlg_abrir.getSaveFileName(None, 'Guardar Copia', copia, '.zip')

            if dlg_abrir.accepted and filename != '':
                print("Guardando backup " + copia + " en " + str(directorio))

                fichzip = zipfile.ZipFile(copia, "w")
                fichzip.write("bbdd.sqlite", os.path.basename("bbdd.sqlite"), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(copia), str(directorio))

                Eventos.lanzar_aviso("Backup guardado")

        except Exception as error:

            print("Error al intentar hacer una copìa de seguridad ", error)

    @staticmethod
    def restaurar_backup():

        try:

            dlg_abrir = views.views.FileDialogAbrir()

            filename = dlg_abrir.getOpenFileName(None, "Restaurar Copia Seguridad", os.getcwd(),
                                                 '*.zip', 'All Files')

            if dlg_abrir.accept and filename[0] != '':
                file = filename[0]

                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)

                bbdd.close()
                conexion.Conexion.conexion()

                Eventos.lanzar_aviso("Copia de seguridad restaurada")

        except Exception as error:

            print("Error al restaurar backup", error)

    @staticmethod
    def importar_datos_excel():

        try:

            dlg_abrir = views.views.FileDialogAbrir()

            filenames = dlg_abrir.getOpenFileName(None, "Importar datos", '',
                                                  '*.xls;;All Files (*)')

            if dlg_abrir.accept and len(filenames) != 0:

                file = filenames[0]

                documento = xlrd.open_workbook(file)
                hojas = documento.sheets()

                for hoja in hojas:

                    if hoja.name == "Clientes":

                        Eventos.importar_hoja_clientes(hoja)

                    elif hoja.name == "Coches":

                        Eventos.importar_hoja_coches(hoja)

                    elif hoja.name == "Productos":

                        Eventos.importar_hoja_clientes(hoja)

                Eventos.lanzar_aviso("Se han importado los datos")

        except Exception as error:

            print("Error al importar datos", error)

    @staticmethod
    def importar_hoja_productos(hoja: xlrd.sheet.Sheet) -> bool:

        out = False

        try:

            for i in range(hoja.nrows):

                if i == 0:

                    # Fila de título de los campos

                    pass

                else:

                    prod_imp = []
                    obj_prod: Servicio

                    for j in range(hoja.ncols):

                        prod_imp.append(str(hoja.cell_value(i, j)))

                    obj_prod = Servicio(prod_imp[1], prod_imp[2], prod_imp[0])

                    out = conexion.Conexion.guardar_servicio(obj_prod)

        except Exception as error:

            print("Error al importar la hoja de productos", error)

        return out

    @staticmethod
    def importar_hoja_clientes(hoja: xlrd.sheet.Sheet) -> bool:

        out = False

        try:

            for i in range(hoja.nrows):

                if i == 0:

                    # Fila de título de los campos

                    pass

                else:

                    cliente_imp = []
                    obj_cliente: Cliente

                    for j in range(hoja.ncols):
                        cliente_imp.append(str(hoja.cell_value(i, j)))

                    obj_cliente = Cliente(dni=cliente_imp[0], nombre=cliente_imp[1], alta=cliente_imp[2],
                                          direccion=cliente_imp[3], provincia=cliente_imp[4], municipio=cliente_imp[5],
                                          pago=cliente_imp[6])

                    out = conexion.Conexion.insertar_cliente(obj_cliente)

        except Exception as error:

            print("Error al importar la hoja de clientes", error)

        return out

    @staticmethod
    def importar_hoja_coches(hoja: xlrd.sheet.Sheet):

        try:

            for i in range(hoja.nrows):

                if i != 0:

                    coche_imp = []
                    obj_coche: Coche

                    for j in range(hoja.ncols):
                        coche_imp.append(str(hoja.cell_value(i, j)))

                    if ajustes_ui.validar_dni(str(coche_imp[0])):
                        pass
                        # Primero validar

                    obj_coche = Coche(matricula=coche_imp[0], dnicli=coche_imp[1], marca=coche_imp[2],
                                      modelo=coche_imp[3], motor=coche_imp[4])

                    conexion.Conexion.insertarCoche(obj_coche)

        except Exception as error:

            print("Error al importar la hoja de clientes", error)
