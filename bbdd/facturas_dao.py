import typing


from bbdd.servicios_dao import ServicioDAO
from models.factura import Factura
from PyQt6 import QtSql

from datetime import datetime
from models.venta_servicio import VentaServicio


class FacturaDAO:

    @staticmethod
    def buscar_facturas_por_id(id_fact: int) -> typing.List[Factura]:
        """
        Busca facturas a partir del id
        :param id_fact: el Id de la factura
        :return: las facturas con Id similar
        """

        out = []

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select id, dni, matricula, fechafac from facturas where id = :id")

            query.bindValue(":id", id_fact)

            if query.exec():

                while query.next():

                    out.append(FacturaDAO.__parse_factura(query))

        except Exception as error:

            print("Error al buscar facturas por DNI", error)

        return out

    @staticmethod
    def buscar_facturas_por_dni(dni: str) -> typing.List[Factura]:
        """
        Busca facturas por dni similares
        :param dni: el dni para buscar
        :return: la lista de Facturas
        """

        out = []

        try:

            query = QtSql.QSqlQuery()

            dni = "%" + dni + "%"

            query.prepare("select id, dni, matricula, fechafac from facturas where dni like :dni")

            query.bindValue(":dni", dni)

            if query.exec():

                while query.next():

                    out.append(FacturaDAO.__parse_factura(query))

        except Exception as error:

            print("Error al buscar facturas por DNI", error)

        return out

    @staticmethod
    def obtener_factura_por_id(id_fact: int) -> Factura:
        """
        Obtiene una factura a partir de su id
        :param id_fact: el id de la factura
        :return: una Factura o None si no se encuentra
        """

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select id, dni, matricula, fechafac from facturas where id = :id")

            query.bindValue(":id", id_fact)

            if query.exec():

                query.next()

                return FacturaDAO.__parse_factura(query)

        except Exception as error:

            print("Error al obtener una factura por id", error)

        return None

    @staticmethod
    def obtener_facturas() -> typing.List[Factura]:
        """
        Obtiene todas las facturas
        :return: la lista con todas las facturas en la base de datos
        """

        out = []

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select id, dni, matricula, fechafac from facturas")

            if query.exec():

                while query.next():

                    out.append(FacturaDAO.__parse_factura(query))

        except Exception as error:

            print("Error al cargar las facturas", error)

        return out

    @staticmethod
    def cargar_servicios_de_factura(idfact: int) -> typing.List[VentaServicio]:
        """
        Carga los servicios de una factura a partir de su id
        :param idfact: el id de la factura
        :return: la lista de servicios
        """

        out = []

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select unidades, id_servicio from facturas_servicios where id_fact = :idfact")
            query.bindValue(":idfact", idfact)

            if query.exec():

                while query.next():

                    id_serv = query.value("id_servicio")
                    unidades = query.value("unidades")

                    servicio = ServicioDAO.cargar_servicio_por_id(id_serv)

                    preciostr = servicio.precio_unidad.replace(",", ".")
                    precio = float(preciostr)

                    out.append(VentaServicio(unidades, servicio.concepto, precio))

        except Exception as error:

            print("Error al cargar servicios de factura", error)

        return out

    @staticmethod
    def obtener_factura_por_dni(dni: str) -> Factura:
        """
        Obtiene una factura a partir de su dni
        :param dni: el dni de la factura
        :return: una Factura o None si no se encuentra
        """

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select * from facturas where dni = :dni")
            query.bindValue(":dni", dni)

            if query.exec():

                return FacturaDAO.__parse_factura(query)

        except Exception as error:

            print("Error al obtener una factura por DNI", error)

        return None

    @staticmethod
    def guardar_venta_factura(idfact: int, idserv: int, unidades: int) -> int:
        """
        Guarda una venta dentro de una factura
        :param idfact: el id de la factura
        :param idserv: el id del servicio
        :param unidades: el número de unidades
        :return: el id de la venta registrada o -1 si no se pudo registrar
        """

        try:

            query = QtSql.QSqlQuery()

            query.prepare("insert into facturas_servicios (id_fact, id_servicio, unidades) values (:idfact, :idserv, :unidades)")

            query.bindValue(":idfact", idfact)
            query.bindValue(":idserv", idserv)
            query.bindValue(":unidades", unidades)

            if query.exec():

                return query.lastInsertId()

        except Exception as error:

            print("Error al guardar las ventas de la factura", error)

        return -1

    @staticmethod
    def crear_factura(dni: str, matricula: str, fecha: str) -> int:
        """
        Crea una factura
        :param dni: el dni del cliente
        :param matricula: la matrícula
        :param fecha: la fecha de creación
        :return: el id de la nueva factura
        """

        try:

            if fecha == "":

                dt = datetime.today()
                fecha = dt.strftime('%d/%m/%Y - %H:%M:%S')

            query = QtSql.QSqlQuery()

            query.prepare("INSERT INTO facturas (dni, matricula, fechafac) VALUES (:dni, :matricula, :fecha)")

            query.bindValue(":dni", dni)
            query.bindValue(":matricula", matricula)
            query.bindValue(":fecha", fecha)

            if query.exec():

                return query.lastInsertId()

        except Exception as error:

            print("Error al crear una factura", error)

        return -1

    @staticmethod
    def __parse_factura(query: QtSql.QSqlQuery) -> Factura:
        """
        Parsea una factura a partir de una query
        :param query: la query de donde obtener la factura
        :return: la factura o None si no se pudo registrar
        """

        try:

            id = query.value("id")
            dni = query.value("dni")
            matricula = query.value("matricula")
            fecha = query.value("fechafac")

            factura = Factura(id, dni, matricula, fecha)

            return factura

        except Exception as error:

            print("Error al parsear una factura desde query", error)

        return None
