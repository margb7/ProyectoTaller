from PyQt6 import QtSql
from typing import List

import events
from models.models import Cliente, Coche, Servicio
from ventMain import *


class Conexion:

    @staticmethod
    def conexion():

        try:

            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("bbdd.sqlite")

            if not db.open():

                QtWidgets.QMessageBox.critical(None, "No se puede abrir la base de datos",
                                               "Conexión no establecida",
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

        except Exception as error:

            print("Error al conectar con la base de datos", error)

    @staticmethod
    def buscar_servicios_concepto(concepto: str):

        servicios = []

        try:

            query = QtSql.QSqlQuery()

            concepto = "%" + concepto + "%"

            query.prepare("select concepto, precio_unidad, codigo from productos where concepto like :concepto")
            query.bindValue(":concepto", concepto)

            if query.exec():

                while query.next():

                    servicios.append(Servicio(query.value(0), query.value(1), query.value(2)))

        except Exception as error:

            print("Error al cargar servicios por nombre", error)

        return servicios

    @staticmethod
    def modifica_servicio(servicio: Servicio) -> bool:

        out = False

        try:

            query = QtSql.QSqlQuery()
            query.prepare("UPDATE productos set concepto = :concepto, precio_unidad = :precio_unidad where codigo = :codigo")

            query.bindValue(":codigo", servicio.codigo)
            query.bindValue(":concepto", servicio.concepto)
            query.bindValue(":precio_unidad", servicio.precio_unidad)

            out = query.exec()

        except Exception as error:

            print("Error al modificar un servicio", error)

        return out

    @staticmethod
    def borraServicioPorCodigo(codigo: str) -> bool:

        out = False

        try:

            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM productos WHERE codigo = :codigo")
            query.bindValue(":codigo", codigo)

            out = query.exec()

        except Exception as error:

            print("Error al borrar un servicio", error)

        return out

    @staticmethod
    def guardar_servicio(servicio: Servicio) -> bool:

        try:

            query = QtSql.QSqlQuery()

            query.prepare("insert into productos (concepto,precio_unidad) values (:concepto, :precio_unidad)")

            query.bindValue(":concepto", servicio.concepto)
            query.bindValue(":precio_unidad", servicio.precio_unidad)

            return query.exec()

        except Exception as error:

            print("Error al guardar un servicio en la BBDD ", error)
            return False

    @staticmethod
    def cargar_lista_servicios():

        servicios = []

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select concepto, precio_unidad, codigo from productos")

            if query.exec():

                while query.next():

                    servicios.append(Servicio(query.value(0), query.value(1), query.value(2)))

                    print(query.value(0))
                    print(query.value(1))
                    print(query.value(2))

        except Exception as error:

            print("Error al cargar la lista de servicios", error)

        return servicios

    @staticmethod
    def cargar_municipios(provincia: str) -> List[str]:

        out = []

        try:

            muni_id = 0

            query = QtSql.QSqlQuery()
            query.prepare("SELECT id FROM provincias WHERE provincia = :prov")
            query.bindValue(":prov", provincia)

            if query.exec():

                while query.next():

                    muni_id = query.value(0)

            query2 = QtSql.QSqlQuery()
            query2.prepare("select municipio from municipios where provincia_id = :id")
            query2.bindValue(":id", muni_id)

            if query2.exec():

                while query2.next():

                    out.append(query2.value(0))

        except Exception as error:

            print("Error al obtener los municipios", error)

        return out

    @staticmethod
    def cargar_provincias() -> List[str]:

        out = []

        try:

            query = QtSql.QSqlQuery()
            query.prepare("select provincia from provincias")

            if query.exec():

                while query.next():

                    out.append(query.value(0))

        except Exception as error:

            print("Error al cargar las provincias", error)

        return out

    @staticmethod
    def alta_cli(new_cli: Cliente, new_car: Coche) -> bool:

        creado = False

        try:

            print(new_car.dnicli)

            if new_cli.dni != "":

                if not Conexion.existe_dni(new_cli.dni):
                    Conexion.insertar_cliente(new_cli)

                    creado = Conexion.insertarCoche(new_car)

        except Exception as error:

            print("Error al dar de alta a un cliente", error)

        return creado

    @staticmethod
    def existe_dni(dni: str) -> bool:

        out = False

        try:

            query = QtSql.QSqlQuery()
            query.prepare("select dni from clientes where dni = :dni")
            query.bindValue(":dni", dni)

            if query.exec():

                out = query.next()

        except Exception as error:

            print("Error al buscar dni repetido", error)

        return out

    @staticmethod
    def one_cli(dni) -> Cliente:

        registro = None

        try:

            query = QtSql.QSqlQuery()
            query.prepare("SELECT NOMBRE, ALTA, DIRECCION, PROVINCIA, "
                          "MUNICIPIO, PAGO FROM CLIENTES WHERE DNI = :dni")

            query.bindValue(":dni", str(dni))

            if query.exec():

                while query.next():

                    registro = Cliente(dni=dni,
                                       nombre=str(query.value(0)),
                                       alta=str(query.value(1)),
                                       direccion=str(query.value(2)),
                                       provincia=str(query.value(3)),
                                       municipio=str(query.value(4)),
                                       pago=str(query.value(5)))

        except Exception as error:

            print("Error al cargar cliente desde dni", error)

        return registro

    @staticmethod
    def insertar_cliente(cliente: Cliente) -> bool:

        out = True

        try:

            query = QtSql.QSqlQuery()
            query.prepare("insert into clientes (dni, nombre, alta, direccion, provincia, municipio, pago) VALUES "
                          "(:dni, :nombre, :alta, :direccion, :provincia, :municipio, :pago)")

            query.bindValue(":dni", str(cliente.dni))
            query.bindValue(":nombre", str(cliente.nombre))
            query.bindValue(":alta", str(cliente.alta))
            query.bindValue(":direccion", str(cliente.direccion))
            query.bindValue(":provincia", str(cliente.provincia))
            query.bindValue(":municipio", str(cliente.municipio))
            query.bindValue(":pago", str(cliente.pago))

            query.exec()

        except Exception as error:

            out = False
            print("Error al intentar insertar un cliente en la BBDD", error)

        return out

    @staticmethod
    def insertarCoche(coche: Coche) -> bool:

        out = True

        try:

            query = QtSql.QSqlQuery()
            query.prepare("insert into coches (matricula, dnicli, marca, modelo, motor) values (:matricula, "
                          ":dnicli, "
                          ":marca, :modelo, :motor)")

            query.bindValue(":matricula", str(coche.matricula))
            query.bindValue(":dnicli", str(coche.dnicli))
            query.bindValue(":marca", str(coche.marca))
            query.bindValue(":modelo", str(coche.modelo))
            query.bindValue(":motor", str(coche.motor))

            query.exec()

        except Exception as error:

            out = False
            print("Error al intentar insertar un cliente en la BBDD", error)

        return out

    @staticmethod
    def borraCliPorDni(dni: str) -> bool:

        out = True

        try:

            query = QtSql.QSqlQuery()

            query.prepare("DELETE FROM CLIENTES WHERE DNI = :dni")
            query.bindValue(":dni", dni)

            out = query.exec()

        except Exception as error:

            print("Error al intentar borrar un cliente de la BBDD", error)
            out = False

        return out

    @staticmethod
    def borraCochePorMatricula(matricula: str) -> bool:

        out = True

        try:

            query = QtSql.QSqlQuery()

            query.prepare("DELETE FROM COCHES WHERE MATRICULA = :matricula")
            query.bindValue(":matricula", matricula)

            query.exec()

        except Exception as error:

            print("Error al intentar borrar un coche de la BBDD", error)
            out = False

        return out

    @staticmethod
    def cargar_lista_coches():

        out = []

        query = QtSql.QSqlQuery()
        query.prepare("select matricula, dnicli, marca, modelo, motor from coches")

        if query.exec():

            while query.next():

                out.append(Coche(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4)))

        return out

    @staticmethod
    def cargar_lista_clientes() -> List[Cliente]:

        out = []

        try:

            query = QtSql.QSqlQuery()
            query.prepare("select dni, nombre, alta, direccion, provincia, municipio, pago from clientes")

            if query.exec():

                while query.next():
                    out.append(Cliente(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4),
                                       query.value(5), query.value(6)))

        except Exception as error:

            print("Error al cargar los clientes de la base de datos", error)

        return out

    @staticmethod
    def update_cli(cliente: Cliente) -> bool:

        out = False

        try:

            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE CLIENTES SET NOMBRE = :nombre, ALTA = :alta, DIRECCION = :direccion, PROVINCIA = :provincia, "
                "MUNICIPIO = :municipio, PAGO = :pago WHERE DNI = :dni")

            query.bindValue(":nombre", cliente.nombre)
            query.bindValue(":alta", cliente.alta)
            query.bindValue(":direccion", cliente.direccion)
            query.bindValue(":provincia", cliente.provincia)
            query.bindValue(":municipio", cliente.municipio)
            query.bindValue(":pago", cliente.pago)
            query.bindValue(":dni", cliente.dni)

            out = query.exec()

        except Exception as error:

            print("Error al modificar el cliente", error)

        return out

    @staticmethod
    def update_coche(coche: Coche) -> bool:

        out = False

        try:

            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE COCHES SET DNICLI = :dnicli, MARCA = :marca, MODELO = :modelo, MOTOR = :motor, "
                "WHERE MATRICULA = :matricula")

            query.bindValue(":dnicli", coche.dnicli)
            query.bindValue(":marca", coche.marca)
            query.bindValue(":modelo", coche.modelo)
            query.bindValue(":motor", coche.motor)
            query.bindValue(":matricula", coche.matricula)

            out = query.exec()

        except Exception as error:

            print("Error al modificar el coche", error)

        return out

    @staticmethod
    def cargar_lista_conceptos() -> List[str]:

        out = []

        try:

            query = QtSql.QSqlQuery()
            query.prepare("select concepto from productos order by concepto")

            if query.exec():

                while query.next():

                    out.append(str(query.value(0)))

        except Exception as error:

            print("Error al cargar la lista de ventas", error)

        return out

    @staticmethod
    def modifica_cli(cliente: Cliente, coche: Coche) -> bool:

        out = False

        try:

            out = Conexion.update_cli(cliente)

            if not out:

                out = Conexion.update_coche(coche)

            if out:

                events.Eventos.lanzar_aviso("Datos Cliente modificados")

            else:

                events.Eventos.lanzar_error("Error al modificar el cliente")

        except Exception as error:

            print("Error al modificar el cliente y el coche", error)

        return out

    @staticmethod
    def obtener_precio_servicio_por_concepto(concepto: str) -> str:

        try:

            query = QtSql.QSqlQuery()

            query.prepare("select precio_unidad from productos where concepto = :concepto")

            query.bindValue(":concepto", concepto)

            if query.exec() and query.next():

                return query.value(0)

        except Exception as error:

            print("Error al obtener el precio de servicio por concepto", error)

        return "-1"
