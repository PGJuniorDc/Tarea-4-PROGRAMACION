"""
servicios_especificos.py

Módulo encargado de implementar los servicios específicos
del sistema Software FJ.

Implementa:
- Herencia
- Polimorfismo
- Sobrescritura de métodos
- Validaciones
"""

from servicio import Servicio, ServicioError


# =========================================================
# CLASE RESERVA SALA
# =========================================================

class ReservaSala(Servicio):
    """
    Servicio para reserva de salas.
    """

    def __init__(
        self,
        nombre,
        precio_base,
        capacidad,
        disponible=True
    ):

        super().__init__(nombre, precio_base, disponible)

        self._capacidad = self.__validar_capacidad(
            capacidad
        )

    # -----------------------------------------------------
    # VALIDACIONES
    # -----------------------------------------------------

    def __validar_capacidad(self, capacidad):

        if not isinstance(capacidad, int):
            raise ServicioError(
                "La capacidad debe ser un número entero."
            )

        if capacidad <= 0:
            raise ServicioError(
                "La capacidad debe ser mayor a cero."
            )

        return capacidad

    # -----------------------------------------------------
    # MÉTODOS SOBRESCRITOS
    # -----------------------------------------------------

    def calcular_costo(self, horas=1):

        if horas <= 0:
            raise ServicioError(
                "Las horas deben ser mayores a cero."
            )

        return self.get_precio_base() * horas

    def descripcion(self):

        return (
            f"Sala '{self.get_nombre()}' "
            f"con capacidad para "
            f"{self._capacidad} personas."
        )


# =========================================================
# CLASE ALQUILER EQUIPO
# =========================================================

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    """

    def __init__(
        self,
        nombre,
        precio_base,
        tipo_equipo,
        disponible=True
    ):

        super().__init__(nombre, precio_base, disponible)

        self._tipo_equipo = self.__validar_tipo(
            tipo_equipo
        )

    # -----------------------------------------------------
    # VALIDACIONES
    # -----------------------------------------------------

    def __validar_tipo(self, tipo):

        if not isinstance(tipo, str):
            raise ServicioError(
                "El tipo de equipo debe ser texto."
            )

        tipo = tipo.strip()

        if len(tipo) < 3:
            raise ServicioError(
                "Tipo de equipo inválido."
            )

        return tipo.title()

    # -----------------------------------------------------
    # MÉTODOS SOBRESCRITOS
    # -----------------------------------------------------

    def calcular_costo(self, dias=1):

        if dias <= 0:
            raise ServicioError(
                "Los días deben ser mayores a cero."
            )

        costo = self.get_precio_base() * dias

        # Recargo simple
        if dias > 7:
            costo += 50000

        return costo

    def descripcion(self):

        return (
            f"Alquiler de equipo tipo "
            f"{self._tipo_equipo}: "
            f"{self.get_nombre()}."
        )


# =========================================================
# CLASE ASESORIA
# =========================================================

class Asesoria(Servicio):
    """
    Servicio de asesorías especializadas.
    """

    def __init__(
        self,
        nombre,
        precio_base,
        especialidad,
        disponible=True
    ):

        super().__init__(nombre, precio_base, disponible)

        self._especialidad = self.__validar_especialidad(
            especialidad
        )

    # -----------------------------------------------------
    # VALIDACIONES
    # -----------------------------------------------------

    def __validar_especialidad(self, especialidad):

        if not isinstance(especialidad, str):
            raise ServicioError(
                "La especialidad debe ser texto."
            )

        especialidad = especialidad.strip()

        if len(especialidad) < 4:
            raise ServicioError(
                "Especialidad inválida."
            )

        return especialidad.title()

    # -----------------------------------------------------
    # MÉTODOS SOBRESCRITOS
    # -----------------------------------------------------

    def calcular_costo(
        self,
        horas=1,
        incluir_impuesto=False
    ):

        if horas <= 0:
            raise ServicioError(
                "Las horas deben ser mayores a cero."
            )

        costo = self.get_precio_base() * horas

        # Simulación de sobrecarga con parámetro opcional
        if incluir_impuesto:
            costo *= 1.19

        return costo

    def descripcion(self):

        return (
            f"Asesoría especializada en "
            f"{self._especialidad}."
        )


# =============================================================
# PRUEBAS DEL MÓDULO
# =============================================================

if __name__ == "__main__":

    print("\n===== PRUEBAS SERVICIOS ESPECÍFICOS =====")

    # ---------------------------------------------------------
    # RESERVA SALA
    # ---------------------------------------------------------

    try:

        sala = ReservaSala(
            "Sala Ejecutiva",
            80000,
            15
        )

        print("\nSERVICIO CREADO")
        print(sala.mostrar_informacion_base())

        print(sala.descripcion())

        print(
            f"Costo total: "
            f"${sala.calcular_costo(3):,.0f}"
        )

    except ServicioError as error:
        print(f"Error: {error}")

    # ---------------------------------------------------------
    # ALQUILER EQUIPO
    # ---------------------------------------------------------

    try:

        equipo = AlquilerEquipo(
            "Portátil HP",
            50000,
            "Laptop"
        )

        print("\nSERVICIO CREADO")
        print(equipo.mostrar_informacion_base())

        print(equipo.descripcion())

        print(
            f"Costo total: "
            f"${equipo.calcular_costo(10):,.0f}"
        )

    except ServicioError as error:
        print(f"Error: {error}")

    # ---------------------------------------------------------
    # ASESORÍA
    # ---------------------------------------------------------

    try:

        asesoria = Asesoria(
            "Consultoría Python",
            120000,
            "Programación"
        )

        print("\nSERVICIO CREADO")
        print(asesoria.mostrar_informacion_base())

        print(asesoria.descripcion())

        print(
            f"Costo sin impuesto: "
            f"${asesoria.calcular_costo(2):,.0f}"
        )

        print(
            f"Costo con impuesto: "
            f"${asesoria.calcular_costo(2, True):,.0f}"
        )

    except ServicioError as error:
        print(f"Error: {error}")

    # ---------------------------------------------------------
    # ERROR INTENCIONAL
    # ---------------------------------------------------------

    try:

        servicio_error = ReservaSala(
            "A",
            -1000,
            -5
        )

    except ServicioError as error:
        print(f"\nError detectado: {error}")