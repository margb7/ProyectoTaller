import os
import platform
import subprocess

from reportlab.pdfgen import canvas
from datetime import datetime


class Informe:

    @staticmethod
    def generar_informe_clientes() -> None:

        try:

            report = canvas.Canvas('informes/listadoCliente.pdf')
            report.setTitle("Informe de Clientes")

            Informe.__generar_titulo_pagina(report, "Clientes")

            Informe.__generar_pie_informe(report, "Clientes")

            report.save()

            root_path = os.path.join(".", "informes")
            root_path += os.sep

            for file in os.listdir(root_path):

                if file.endswith("Cliente.pdf"):

                    if platform.system() == "Windows":

                        os.startfile(os.path.join(root_path, file))

                    else:

                        subprocess.call(("xdg-open", os.path.join(root_path, file)))

        except Exception as error:

            print("Error informes de estado de clientes", error)

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
    def __generar_titulo_pagina(canvas: canvas.Canvas, titulo: str):

        try:

            canvas.setFontSize(22)
            canvas.drawString(75, 760, titulo)
            canvas.line(50, 750, 525, 750)

        except Exception as error:

            print("Error al generar el título de la página", error)

    @staticmethod
    def __generar_pie_informe(canvas: canvas.Canvas, titulo: str) -> None:

        try:

            canvas.line(50, 50, 525, 50)
            canvas.setFontSize(7)

            fecha = datetime.today()
            fecha = fecha.strftime("%d.%m.%Y - %H:%M")

            # canvas.setFont("Ubuntu", size=7)

            canvas.drawString(50, 40, str(fecha))
            canvas.drawString(475, 40, "Página " + str(canvas.getPageNumber()))
            canvas.drawString(250, 40, titulo)

        except Exception as error:

            print("Error al colocar el pie de página", error)
