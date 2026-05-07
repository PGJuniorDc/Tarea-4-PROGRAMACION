"""
servicio.py

Clase abstracta base para todos los servicios del sistema.
Implementa abstracción, herencia y polimorfismo.
"""

from abc import ABC, abstractmethod


class ServicioError(Exception):
    """
    Excepción personalizada para errores relacionados
    con los servicios del sistema.
    """
    pass


class Servicio(ABC):
    """
    Clase abstracta que representa un servicio general.

    Esta clase sirve como base para:
    - ReservaSala
    - AlquilerEquipo
    - Asesoria

    Implementa:
    - Abstracción
    - Herencia
    - Polimorfismo
    """

    def __init__(self, nombre, precio_base, disponible=True):
        """
        Constructor de la clase Servicio.

        Args:
            nombre (str): Nombre del servicio.
            precio_base (float): Precio base del servicio.
            disponible (bool): Disponibilidad del servicio.
        """

        self._nombre = self.__validar_nombre(nombre)
        self._precio_base = self.__validar_precio(precio_base)
        self._disponible = disponible

    # =========================================================
    # VALIDACIONES PRIVADAS
    # =========================================================

    def __validar_nombre(self, nombre):
        """
        Valida el nombre del servicio.
        """

        if not isinstance(nombre, str):
            raise ServicioError(
                "El nombre del servicio debe ser texto."
            )

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise ServicioError(
                "El nombre del servicio es demasiado corto."
            )

        return nombre.title()

    def __validar_precio(self, precio):
        """
        Valida el precio base del servicio.
        """

        if not isinstance(precio, (int, float)):
            raise ServicioError(
                "El precio debe ser numérico."
            )

        if precio <= 0:
            raise ServicioError(
                "El precio debe ser mayor que cero."
            )

        return float(precio)

    # =========================================================
    # GETTERS
    # =========================================================

    def get_nombre(self):
        return self._nombre

    def get_precio_base(self):
        return self._precio_base

    def esta_disponible(self):
        return self._disponible

    # =========================================================
    # SETTERS
    # =========================================================

    def set_nombre(self, nuevo_nombre):
        self._nombre = self.__validar_nombre(nuevo_nombre)

    def set_precio_base(self, nuevo_precio):
        self._precio_base = self.__validar_precio(nuevo_precio)

    def cambiar_disponibilidad(self, estado):
        """
        Cambia la disponibilidad del servicio.
        """

        if not isinstance(estado, bool):
            raise ServicioError(
                "La disponibilidad debe ser True o False."
            )

        self._disponible = estado

    # =========================================================
    # MÉTODOS ABSTRACTOS
    # =========================================================

    @abstractmethod
    def calcular_costo(self):
        """
        Método abstracto para calcular el costo total.
        Cada servicio debe implementar su propia lógica.
        """
        pass

    @abstractmethod
    def descripcion(self):
        """
        Método abstracto para describir el servicio.
        """
        pass

    # =========================================================
    # MÉTODOS GENERALES
    # =========================================================

    def mostrar_informacion_base(self):
        """
        Retorna información básica del servicio.
        """

        estado = (
            "Disponible"
            if self._disponible
            else "No disponible"
        )

        return (
            f"\n===== INFORMACIÓN DEL SERVICIO =====\n"
            f"Nombre: {self._nombre}\n"
            f"Precio base: ${self._precio_base:,.2f}\n"
            f"Estado: {estado}\n"
        )

    def verificar_disponibilidad(self):
        """
        Verifica si el servicio está disponible.
        """

        if not self._disponible:
            raise ServicioError(
                f"El servicio '{self._nombre}' "
                f"no se encuentra disponible."
            )

        return True

    # =========================================================
    # MÉTODOS ESPECIALES
    # =========================================================

    def __str__(self):
        """
        Representación amigable del objeto.
        """

        return (
            f"Servicio(nombre='{self._nombre}', "
            f"precio_base={self._precio_base})"
        )

    def __repr__(self):
        """
        Representación técnica del objeto.
        """

        return self.__str__()


# =============================================================
# PRUEBAS DEL MÓDULO
# =============================================================

if __name__ == "__main__":

    print("\n===== PRUEBAS DE LA CLASE SERVICIO =====")

    # ---------------------------------------------------------
    # Clase temporal para pruebas
    # ---------------------------------------------------------

    class ServicioPrueba(Servicio):

        def calcular_costo(self):
            return self.get_precio_base() * 1.19

        def descripcion(self):
            return (
                f"Servicio de prueba: {self.get_nombre()}"
            )

    # ---------------------------------------------------------
    # CASO 1: Servicio válido
    # ---------------------------------------------------------

    try:

        servicio1 = ServicioPrueba(
            "Servicio General",
            50000
        )

        print("\nServicio creado correctamente")
        print(servicio1.mostrar_informacion_base())

        print("Costo total:")
        print(servicio1.calcular_costo())

        print("\nDescripción:")
        print(servicio1.descripcion())

    except ServicioError as error:
        print(f"Error: {error}")

    # ---------------------------------------------------------
    # CASO 2: Precio inválido
    # ---------------------------------------------------------

    try:

        servicio2 = ServicioPrueba(
            "Servicio Incorrecto",
            -1000
        )

    except ServicioError as error:
        print(f"\nError detectado: {error}")

    # ---------------------------------------------------------
    # CASO 3: Servicio no disponible
    # ---------------------------------------------------------

    try:

        servicio1.cambiar_disponibilidad(False)
        servicio1.verificar_disponibilidad()

    except ServicioError as error:
        print(f"\nError detectado: {error}")