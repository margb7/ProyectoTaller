import os
import platform
import subprocess
import typing

from reportlab.pdfgen import canvas
from datetime import datetime
from .factura import Factura

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

import conexion


class Informe:
    """
    Clase para manejar y crear informes
    """

    @staticmethod
    def generar_informe_clientes() -> None:
        """
        Genera el informe de clientes
        :return: None
        """

        try:

            listado_clientes = conexion.Conexion.cargar_lista_clientes()

            # Crear la lista de datos
            data = [
                ['DNI', 'Nombre', 'Dirección', 'Provincia', 'Municipio'],
            ]

            for cliente in listado_clientes:

                str_dni = "*" * 4 + cliente.dni[4:]

                data.append([str_dni, cliente.nombre, cliente.direccion, cliente.provincia, cliente.municipio])

            # Crear el documento PDF y el objeto canvas
            pdf = canvas.Canvas('informes/listadoClientes.pdf', pagesize=A4)
            pdf.setTitle("Informe de Clientes")

            Informe.__generar_titulo_pagina(pdf, "Listado de clientes")
            Informe.__generar_pie_informe(pdf, "LISTADO CLIENTES")

            # Crear la tabla y darle formato
            table_width = A4[0] * 0.95
            table_left_margin = (A4[0] - table_width) / 2
            table = Table(data, colWidths=[table_width / 5] * 5)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))

            # Obtener la altura total de la tabla
            table_height = len(data) * 30  # 30 es la altura predeterminada de cada fila

            # Añadir la tabla al documento PDF y cerrarlo
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, table_left_margin,
                         10.05 * inch - table_height)  # Agregar 0.5 pulgadas a la altura del encabezado
            pdf.save()

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
    def generar_informe_vehiculos() -> None:
        """
        Genera un informe con los vehículos
        :return: None
        """

        try:

            # Crear la lista de datos

            data = [
                ['DNI', 'Matrícula', 'Marca', 'Modelo', 'Motor'],
            ]

            lista_vehiculos = conexion.Conexion.cargar_lista_coches()

            for v in lista_vehiculos:

                data.append([v.dnicli, v.matricula, v.marca, v.modelo, v.motor])

            # Crear el documento PDF y el objeto canvas
            pdf = canvas.Canvas('informes/listadoVehiculos.pdf')
            pdf.setTitle("Listado de Vehículos")

            Informe.__generar_titulo_pagina(pdf, "Vehículos")

            # Crear la tabla y darle formato
            table_width = A4[0] * 0.8
            table_left_margin = (A4[0] - table_width) / 2 - 10
            table = Table(data, colWidths=[table_width / 5] * 5)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))

            # Obtener la altura total de la tabla
            table_height = len(data) * 30  # 30 es la altura predeterminada de cada fila

            # Añadir la tabla al documento PDF y cerrarlo
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, table_left_margin, 10.2 * inch - table_height)

            Informe.__generar_pie_informe(pdf, "Vehículos")

            pdf.save()

            root_path = os.path.join(".", "informes")
            root_path += os.sep

            for file in os.listdir(root_path):

                if file.endswith("Vehiculos.pdf"):

                    if platform.system() == "Windows":

                        os.startfile(os.path.join(root_path, file))

                    else:

                        subprocess.call(("xdg-open", os.path.join(root_path, file)))

        except Exception as error:

            print("Error al generar el informe de vehículos", error)

    @staticmethod
    def generar_informe_factura(factura: Factura, conceptos: typing.List[str], unidades: typing.List[float],
                                precios: typing.List[str]):
        """
        Genera un informe de una factura
        :param factura: la factura para crear el informe
        :param conceptos: la lista de conceptos de la factura
        :param unidades: la lista de unidades de la factura
        :param precios: la lista de precios de la factura
        :return: None
        """

        try:

            nombre = f"factura_{factura.dni}_{factura.id_factura}.pdf"

            report = canvas.Canvas(f'informes/{nombre}')
            report.setTitle("Factura")

            Informe.__generar_titulo_pagina(report, "Factura")

            Informe.__generar_pie_informe(report, "Factura")

            report.setFont("Helvetica-Bold", size=11)

            report.drawString(50, 700, "Datos cliente")

            report.setFont("Helvetica", size=8)
            report.drawString(55, 675, "- DNI:")
            report.drawString(150, 675, factura.dni)

            report.drawString(55, 660, "- Matrícula:")
            report.drawString(150, 660, factura.matricula)

            report.drawString(55, 645, "- Fecha factura:")
            report.drawString(150, 645, factura.fecha_factura)

            report.drawString(55, 630, "- Número factura:")
            report.drawString(150, 630, str(factura.id_factura))
            report.line(50, 620, 525, 620)

            report.setFont("Helvetica-Bold", size=11)
            report.drawString(50, 600, "Servicios contratados")
            report.setFont("Helvetica", size=8)

            Informe.__mostrar_productos(report, conceptos, unidades, precios)

            report.save()

            root_path = os.path.join(".", "informes")
            root_path += os.sep

            for file in os.listdir(root_path):

                if file.endswith(nombre):

                    if platform.system() == "Windows":

                        os.startfile(os.path.join(root_path, file))

                    else:

                        subprocess.call(("xdg-open", os.path.join(root_path, file)))

        except Exception as error:

            print("Error al generar el informe de la factura", error)


    @staticmethod
    def __mostrar_productos(page: canvas.Canvas, conceptos: typing.List[str], unidades: typing.List[float],
                            precios: typing.List[str]):
        """
        Coloca la lista de productos en un documento
        :param page: el documento donde colocar los productos
        :param conceptos: los conceptos que colocar
        :param unidades: las unidades que colocar
        :param precios: los precios que colocar
        :return: None
        """

        try:

            numeros = len(conceptos)

            pos_y = 580

            diff = 20
            distancia_x = [50, 300, 350, 425]

            Informe.__cabecera_servicios(page, distancia_x, pos_y)

            pos_y -= diff

            for i in range(numeros):
                page.drawString(distancia_x[0], pos_y, str(conceptos[i]))
                page.drawString(distancia_x[1], pos_y, str(precios[i]))
                page.drawString(distancia_x[2], pos_y, str(unidades[i]))

                precio = precios[i].replace(",", ".")
                unidad = str(unidades[i])

                unidad = unidad.replace(",", ".")

                subtotal = float(precio) * float(unidad)

                page.drawString(distancia_x[3], pos_y, "{:.2f}".format(subtotal))

                pos_y -= diff


        except Exception as error:

            print("Error al guardar los conceptos en la factura", error)


    @staticmethod
    def __cabecera_servicios(page: canvas.Canvas, distancias, y):
        """
        Coloca la cabecera de servicios en un documento
        :param page: el documento
        :param distancias: las distancias para colocar los diferentes títulos
        :param y: la altura donde colocar los titulos
        :return: None
        """

        try:

            page.setFont("Helvetica-Bold", size=11)

            page.drawString(distancias[0], y, "Concepto")
            page.drawString(distancias[1], y, "Precio")
            page.drawString(distancias[2], y, "Unidades")
            page.drawString(distancias[3], y, "Subtotal")

        except Exception as error:

            print("Error al crear la cabecera de servicios", error)

        page.setFont("Helvetica", size=8)


    @staticmethod
    def __generar_titulo_pagina(page: canvas.Canvas, titulo: str):
        """
        Coloca el título de la página e información de la empresa en el documento
        :param page: el documento
        :param titulo: el título
        :return: None
        """

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

            page.setFont("Helvetica-Bold", 12)
            page.drawString(75, 725, titulo)
            page.line(50, 715, 525, 715)

        except Exception as error:

            print("Error al generar el título de la página", error)


    @staticmethod
    def __generar_pie_informe(page: canvas.Canvas, titulo: str) -> None:
        """
        Genera el pie del documento
        :param page: el documento
        :param titulo: el título del documento
        :return: None
        """

        try:

            page.line(50, 50, 525, 50)
            page.setFontSize(7)

            fecha = datetime.today()
            fecha = fecha.strftime("%d/%m/%Y - %H:%M")

            page.drawString(50, 40, str(fecha))
            page.drawString(475, 40, "Página " + str(page.getPageNumber()))
            page.drawString(250, 40, titulo)

        except Exception as error:

            print("Error al colocar el pie de página", error)
