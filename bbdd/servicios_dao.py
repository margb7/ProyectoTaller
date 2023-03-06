from models.models import Servicio
from PyQt6 import QtSql


class ServicioDAO:

    @staticmethod
    def cargar_servicio_por_concepto(concepto: str) -> Servicio:
        """
        Carga un servicio a partir de un concepto
        :param concepto: el concepto
        :return: el servicio o None si no se encuentra
        """

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select concepto, precio_unidad, codigo from productos where concepto = :concepto")
            query.bindValue(":concepto", concepto)

            if query.exec():

                query.next()

                return Servicio(query.value(0), query.value(1), query.value(2))

        except Exception as error:

            print("Error al cargar un servicio por concepto", error)

        return None

    @staticmethod
    def cargar_servicio_por_id(idserv: int) -> Servicio:
        """
        Carga un servicio a partir de su id
        :idserv: el id
        :return: el servicio o None si no se encuentra
        """

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select concepto, precio_unidad, codigo from productos where codigo = :idserv")
            query.bindValue(":idserv", idserv)

            if query.exec():

                query.next()

                return Servicio(query.value(0), query.value(1), query.value(2))

        except Exception as error:

            print("Error al cargar un servicio por concepto", error)

        return None
