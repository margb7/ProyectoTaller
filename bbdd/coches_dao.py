import typing
from models.models import Coche


class CochesDAO:

    @staticmethod
    def buscarPorDni(dnicli: str) -> typing.List[Coche]:

        out = []

        try:



            query = QtSql.QSqlQuery()
            query.prepare("select matricula, dnicli, marca, modelo, motor from coches where dnicli like %:dnicli%")

            if query.exec():

                while query.next():

                    out.append(Coche(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4)))

        except Exception as error:

            print("Error al buscar un coche por dni de cliente", error)

        return out
