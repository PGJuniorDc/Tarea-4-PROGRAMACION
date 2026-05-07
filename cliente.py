"""
cliente.py

Módulo encargado de gestionar la información de los clientes.
Implementa encapsulación, validaciones robustas y manejo de excepciones.
"""

import re
from datetime import datetime


class ClienteError(Exception):
    """Excepción personalizada para errores relacionados con clientes."""
    pass


class Cliente:
    """
    Clase que representa un cliente dentro del sistema.

    Características implementadas:
    - Encapsulación de atributos
    - Validaciones robustas
    - Métodos de acceso controlado
    - Métodos para mostrar y actualizar información
    - Manejo de excepciones
    """

    def __init__(self, nombre, correo, telefono, identificacion):
        """
        Constructor de la clase Cliente.

        Args:
            nombre (str): Nombre completo del cliente.
            correo (str): Correo electrónico.
            telefono (str): Número telefónico.
            identificacion (str): Documento o identificación.
        """

        # Encapsulación de atributos
        self.__nombre = None
        self.__correo = None
        self.__telefono = None
        self.__identificacion = None
        self.__fecha_registro = datetime.now()

        # Validaciones mediante setters
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)
        self.set_identificacion(identificacion)

    # =========================================================
    # VALIDACIONES PRIVADAS
    # =========================================================

    def __validar_nombre(self, nombre):
        """Valida el nombre del cliente."""

        if not isinstance(nombre, str):
            raise ClienteError("El nombre debe ser texto.")

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise ClienteError(
                "El nombre debe tener al menos 3 caracteres."
            )

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', nombre):
            raise ClienteError(
                "El nombre solo puede contener letras y espacios."
            )

        return nombre.title()

    def __validar_correo(self, correo):
        """Valida el correo electrónico."""

        if not isinstance(correo, str):
            raise ClienteError("El correo debe ser texto.")

        correo = correo.strip()

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(patron, correo):
            raise ClienteError("Correo electrónico inválido.")

        return correo.lower()

    def __validar_telefono(self, telefono):
        """Valida el número telefónico."""

        telefono = str(telefono).strip()

        if not telefono.isdigit():
            raise ClienteError(
                "El teléfono solo debe contener números."
            )

        if len(telefono) < 7 or len(telefono) > 15:
            raise ClienteError(
                "El teléfono debe tener entre 7 y 15 dígitos."
            )

        return telefono

    def __validar_identificacion(self, identificacion):
        """Valida la identificación del cliente."""

        identificacion = str(identificacion).strip()

        if not identificacion.isdigit():
            raise ClienteError(
                "La identificación debe contener solo números."
            )

        if len(identificacion) < 5:
            raise ClienteError(
                "La identificación es demasiado corta."
            )

        return identificacion

    # =========================================================
    # GETTERS
    # =========================================================

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def get_telefono(self):
        return self.__telefono

    def get_identificacion(self):
        return self.__identificacion

    def get_fecha_registro(self):
        return self.__fecha_registro.strftime("%Y-%m-%d %H:%M:%S")

    # =========================================================
    # SETTERS
    # =========================================================

    def set_nombre(self, nombre):
        self.__nombre = self.__validar_nombre(nombre)

    def set_correo(self, correo):
        self.__correo = self.__validar_correo(correo)

    def set_telefono(self, telefono):
        self.__telefono = self.__validar_telefono(telefono)

    def set_identificacion(self, identificacion):
        self.__identificacion = self.__validar_identificacion(
            identificacion
        )

    # =========================================================
    # MÉTODOS PRINCIPALES
    # =========================================================

    def mostrar_informacion(self):
        """Muestra la información completa del cliente."""

        informacion = (
            f"\n===== INFORMACIÓN DEL CLIENTE =====\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo: {self.__correo}\n"
            f"Teléfono: {self.__telefono}\n"
            f"Identificación: {self.__identificacion}\n"
            f"Fecha de registro: {self.get_fecha_registro()}\n"
        )

        return informacion

    def actualizar_correo(self, nuevo_correo):
        """Actualiza el correo electrónico del cliente."""

        correo_anterior = self.__correo
        self.set_correo(nuevo_correo)

        return (
            f"Correo actualizado correctamente:\n"
            f"Anterior: {correo_anterior}\n"
            f"Nuevo: {self.__correo}"
        )

    def actualizar_telefono(self, nuevo_telefono):
        """Actualiza el número telefónico del cliente."""

        telefono_anterior = self.__telefono
        self.set_telefono(nuevo_telefono)

        return (
            f"Teléfono actualizado correctamente:\n"
            f"Anterior: {telefono_anterior}\n"
            f"Nuevo: {self.__telefono}"
        )

    # =========================================================
    # MÉTODOS ESPECIALES
    # =========================================================

    def __str__(self):
        """Representación amigable del objeto."""

        return (
            f"Cliente(nombre='{self.__nombre}', "
            f"correo='{self.__correo}')"
        )

    def __repr__(self):
        """Representación técnica del objeto."""

        return self.__str__()


# =============================================================
# PRUEBAS DEL MÓDULO
# =============================================================

if __name__ == "__main__":

    print("\n===== PRUEBAS DEL SISTEMA CLIENTE =====")

    # ---------------------------------------------------------
    # CASO 1: Cliente válido
    # ---------------------------------------------------------

    try:
        cliente1 = Cliente(
            "Andrés López",
            "andres@gmail.com",
            "3201234567",
            "123456789"
        )

        print("\nCliente creado correctamente")
        print(cliente1.mostrar_informacion())

    except ClienteError as error:
        print(f"Error: {error}")

    # ---------------------------------------------------------
    # CASO 2: Nombre inválido
    # ---------------------------------------------------------

    try:
        cliente2 = Cliente(
            "",
            "correo@gmail.com",
            "3201234567",
            "987654321"
        )

    except ClienteError as error:
        print(f"\nError detectado: {error}")

    # ---------------------------------------------------------
    # CASO 3: Correo inválido
    # ---------------------------------------------------------

    try:
        cliente3 = Cliente(
            "Carlos",
            "correo_invalido",
            "3201234567",
            "741852963"
        )

    except ClienteError as error:
        print(f"\nError detectado: {error}")

    # ---------------------------------------------------------
    # CASO 4: Teléfono inválido
    # ---------------------------------------------------------

    try:
        cliente4 = Cliente(
            "Laura",
            "laura@gmail.com",
            "telefono",
            "963852741"
        )

    except ClienteError as error:
        print(f"\nError detectado: {error}")

    # ---------------------------------------------------------
    # CASO 5: Actualización de datos
    # ---------------------------------------------------------

    try:
        cliente1.actualizar_correo("nuevo_correo@gmail.com")
        cliente1.actualizar_telefono("3009876543")

        print("\nDatos actualizados correctamente")
        print(cliente1.mostrar_informacion())

    except ClienteError as error:
        print(f"Error: {error}")
