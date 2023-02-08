import typing

from models.factura import Factura
from PyQt6 import QtSql


class DaoFacturas:

    @staticmethod
    def obtener_facturas() -> typing.List[Factura]:
        out = []

        query = QtSql.QSqlQuery()

        query.prepare("select * from facturas")

        while query.next():

            out.append(DaoFacturas.__parse_factura(query))

        return out

    @staticmethod
    def obtener_factura_por_dni(dni: str) -> Factura:

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select * from facturas where dni = :dni")
            query.bindValue(":dni", dni)

            if query.exec():

                return DaoFacturas.__parse_factura(query)

        except Exception as error:

            print("Error al obtener una factura por DNI", error)

        return None

    @staticmethod
    def __parse_factura(query: QtSql.QSqlQuery) -> Factura:

        try:

            id = query.value(1)
            dni = query.value(2)
            matricula = query.value(3)
            fecha = query.value(4)

            factura = Factura(id, dni, matricula, fecha)

            return factura

        except Exception as error:

            print("Error al parsear una factura desde query", error)

        return None
