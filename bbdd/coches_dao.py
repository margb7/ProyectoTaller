import typing
from models.models import Coche
from PyQt6 import QtSql


class CochesDAO:

    @staticmethod
    def buscarPorDni(dnicli: str) -> typing.List[Coche]:
        """
        Buscar coches por DNI
        :param dnicli: el dni del cliente
        :return: los coches registrados para el dni
        """

        out = []

        try:

            query = QtSql.QSqlQuery()
            query.prepare("select matricula, dnicli, marca, modelo, motor from coches where dnicli like :dnicli")

            dnicli = "%" + dnicli + "%"

            query.bindValue(":dnicli", dnicli)

            if query.exec():

                while query.next():

                    out.append(Coche(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4)))

        except Exception as error:

            print("Error al buscar un coche por dni de cliente", error)

        return out
