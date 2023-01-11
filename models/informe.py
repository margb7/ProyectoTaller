import os
import platform
import subprocess

from reportlab.pdfgen import canvas
from datetime import datetime

import ajustes_ui
import conexion


class Informe:

    @staticmethod
    def generar_informe_clientes() -> None:

        try:

            report = canvas.Canvas('informes/listadoClientes.pdf')
            report.setTitle("Informe de Clientes")

            Informe.__generar_titulo_pagina(report, "Listado de clientes")
            Informe.__generar_pie_informe(report, "LISTADO CLIENTES")

            Informe.__colocar_label_clientes(report)

            listado_clientes = conexion.Conexion.cargar_lista_clientes()

            distancia_x = [60, 120, 270, 370, 460]
            items = ["DNI", "NOMBRE", "DIRECCIÓN", "PROVINCIA", "MUNICIPIO"]
            pixeles_centro = []

            i = 0

            # 16px = 12pt
            for item in distancia_x:

                pixeles_centro.append(item + (ajustes_ui.fuente_a_pixeles(items[i], 10) / 2))
                i += 1

            i = 50
            j = 675

            for cli in listado_clientes:

                if j <= 80:

                    report.drawString(460, 90, "Página siguiente ...")
                    report.showPage()

                    Informe.__generar_titulo_pagina(report, "Listado de clientes")
                    Informe.__generar_pie_informe(report, "LISTADO CLIENTES")
                    Informe.__colocar_label_clientes(report)

                    j = 675
                    i = 50

                report.setFont("Helvetica", size=7)
                report.drawString(i, j, cli.dni)
                report.drawString(ajustes_ui.calcular_inicio_texto_centrado(pixeles_centro[1], cli.nombre, 7), j, cli.nombre)
                report.drawString(i + 225, j, cli.direccion)
                report.drawString(i + 330, j, cli.provincia)
                report.drawString(i + 425, j, cli.municipio)

                j = j - 25

            report.save()

            root_path = os.path.join(".", "informes")
            root_path += os.sep

            for file in os.listdir(root_path):

                if file.endswith("Clientes.pdf"):

                    if platform.system() == "Windows":

                        os.startfile(os.path.join(root_path, file))

                    else:

                        subprocess.call(("xdg-open", os.path.join(root_path, file)))

        except Exception as error:

            print("Error informes de estado de clientes", error)

    @staticmethod
    def __colocar_label_clientes(page: canvas.Canvas):

        items = ["DNI", "NOMBRE", "DIRECCIÓN", "PROVINCIA", "MUNICIPIO"]
        distancia_x = [60, 120, 270, 370, 460]

        page.setFont("Helvetica-Bold", 10)
        i = 0

        for item in items:
            page.drawString(distancia_x[i], 700, item)

            i += 1

        page.line(50, 690, 525, 690)

    @staticmethod
    def generar_informe_vehiculos() -> None:

        try:

            report = canvas.Canvas('informes/listadoVehiculos.pdf')
            report.setTitle("Informe de Clientes")

            Informe.__generar_titulo_pagina(report, "Vehículos")

            Informe.__generar_pie_informe(report, "Vehículos")

            report.save()

            root_path = os.path.join(".", "informes")
            root_path += os.sep

            for file in os.listdir(root_path):

                if file.endswith("Vehiculos.pdf"):

                    if platform.system() == "Windows":

                        os.startfile(os.path.join(root_path, file))

                    else:

                        subprocess.call(("xdg-open", os.path.join(root_path, file)))

        except Exception as error:

            print("Error informes de estado de vehículos", error)

    @staticmethod
    def __generar_titulo_pagina(page: canvas.Canvas, titulo: str):

        try:

            logo_path = "./img/logo_taller.jpg"
            page.line(125, 800, 525, 800)

            page.setFont("Helvetica-Bold", 14)

            info_x = 125

            page.drawString(info_x, 810, "Taller mecánico Teis")
            page.drawImage(logo_path, 30, 765, mask="auto", width=80, height=50)

            page.setFont("Helvetica-Bold", 7)
            page.setFillColor("gray")

            page.drawString(info_x, 790, "CIF: A12345678")
            page.drawString(info_x, 780, "Avda. Galicia - 101")
            page.drawString(info_x, 770, "Vigo - 36216")
            page.drawString(info_x, 760, "e-mail: mitaller@gmail.com - Telf: 986 132 456")

            page.setFillColor("black")

            page.setFont("Helvetica-Bold", 10)
            page.drawString(75, 725, titulo)
            page.line(50, 715, 525, 715)

        except Exception as error:

            print("Error al generar el título de la página", error)

    @staticmethod
    def __generar_pie_informe(page: canvas.Canvas, titulo: str) -> None:

        try:

            page.line(50, 50, 525, 50)
            page.setFontSize(7)

            fecha = datetime.today()
            fecha = fecha.strftime("%d/%m/%Y - %H:%M")

            # canvas.setFont("Ubuntu", size=7)

            page.drawString(50, 40, str(fecha))
            page.drawString(475, 40, "Página " + str(page.getPageNumber()))
            page.drawString(250, 40, titulo)

        except Exception as error:

            print("Error al colocar el pie de página", error)
