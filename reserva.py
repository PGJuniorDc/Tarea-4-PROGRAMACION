
"""
reserva.py

Módulo encargado de gestionar las reservas del sistema.
Implementa encapsulación rigurosa y validación en la instanciación.
"""

from servicio import Servicio
from excepciones import ReservaError, GestorLogs
import datetime
from servicio import Servicio, ServicioError # Importamos ServicioError para capturarlo
from excepciones import ReservaError, DisponibilidadError, GestorLogs


class Reserva:
    """
    Clase que representa una reserva en el sistema de Software FJ.
    Integra a un cliente, el servicio solicitado, la duración y controla el estado.
    """

    def __init__(self, cliente, servicio, duracion_horas):
        """
        Constructor de la clase Reserva.

        Args:
            cliente (Cliente): Objeto de la clase Cliente (que construiremos luego).
            servicio (Servicio): Objeto que herede de la clase Servicio.
            duracion_horas (int/float): Tiempo de reserva.
        """
        # Encapsulación de atributos protegidos
        self._cliente = cliente
        self._servicio = self.__validar_servicio(servicio)
        self._duracion_horas = self.__validar_duracion(duracion_horas)
        self._estado = "Pendiente"  # Todas las reservas inician en estado Pendiente
        self._fecha_creacion = datetime.datetime.now()

    # =========================================================
    # VALIDACIONES PRIVADAS (ENCAPSULACIÓN DE COMPORTAMIENTO)
    # =========================================================

    def __validar_servicio(self, servicio):
        """
        Valida que el servicio pasado sea realmente una instancia de la clase Servicio.
        """
        if not isinstance(servicio, Servicio):
            GestorLogs.registrar_error(
                "ReservaError", 
                "Se intentó crear una reserva con un servicio inválido.", 
                "Clase Reserva - __init__"
            )
            raise ReservaError("El servicio proporcionado no es válido en el sistema.")
        return servicio

    def __validar_duracion(self, duracion):
        """
        Valida que la duración de la reserva sea un número lógico y mayor a cero.
        """
        if not isinstance(duracion, (int, float)):
            raise ReservaError("La duración de la reserva debe ser un valor numérico.")
        
        if duracion <= 0:
            raise ReservaError("La duración de la reserva debe ser mayor a cero.")
            
        return float(duracion)
    
    # =========================================================
    # MÉTODOS DE PROCESAMIENTO (LÓGICA DE NEGOCIO)
    # =========================================================

    def confirmar_reserva(self):
        """
        Intenta confirmar la reserva validando la disponibilidad del servicio.
        Aplica try/except/else/finally y encadenamiento de excepciones.
        """
        print(f"\n[SISTEMA] Iniciando confirmación para: {self._servicio.get_nombre()}...")

        try:
            # Intentamos verificar si el servicio está disponible (definido en servicio.py)
            self._servicio.verificar_disponibilidad()
            
        except ServicioError as e:
            # Si el servicio lanza un error, lo 'encadenamos' a nuestra DisponibilidadError
            mensaje = f"Fallo de disponibilidad: {str(e)}"
            
            # Registramos en el archivo logs.txt
            GestorLogs.registrar_error("DisponibilidadError", mensaje, "Reserva.confirmar_reserva")
            
            # Lanzamos la excepción personalizada usando 'from' para encadenamiento profesional
            raise DisponibilidadError(mensaje) from e

        except Exception as e:
            # Captura cualquier otro error inesperado
            GestorLogs.registrar_error("ErrorInesperado", str(e), "Reserva.confirmar_reserva")
            raise ReservaError(f"Error crítico al confirmar: {e}")

        else:
            # El bloque ELSE solo se ejecuta si el TRY fue exitoso (no hubo excepciones)
            self._estado = "Confirmada"
            print(f"✓ ÉXITO: Reserva confirmada para el cliente {self._cliente}.")

        finally:
            # El bloque FINALLY se ejecuta SIEMPRE, haya error o no
            # Ideal para limpiezas o registros finales de auditoría
            print(f"[AUDITORÍA] Proceso de confirmación finalizado para el servicio: {self._servicio.get_nombre()}")


    def cancelar_reserva(self):
        """
        Cancela una reserva existente. Valida que no esté previamente cancelada.
        """
        print(f"\n[SISTEMA] Procesando cancelación de reserva...")

        try:
            # Simulación de validación: No se puede cancelar algo ya cancelado
            if self._estado == "Cancelada":
                raise ReservaError("La reserva ya se encuentra en estado 'Cancelada'.")
            
            # Aquí podrían ir más validaciones (ej. tiempo límite de cancelación)

        except ReservaError as error:
            # Registramos el intento fallido en el log
            GestorLogs.registrar_error("ReservaError", str(error), "Reserva.cancelar_reserva")
            raise # Re-lanzamos para que el programa principal decida qué hacer

        else:
            # Si no hubo errores, cambiamos el estado
            self._estado = "Cancelada"
            print(f"⚠ AVISO: La reserva ha sido cancelada correctamente.")

        finally:
            # Registro de evento en consola para seguimiento del desarrollador
            print(f"[AUDITORÍA] Intento de cambio de estado finalizado. Estado actual: {self._estado}")
            
            
            # =============================================================
# PRUEBAS DEL MÓDULO (SIMULACIÓN DE ESCENARIOS)
# =============================================================

if __name__ == "__main__":
    
    print("\n" + "="*60)
    print("🚀 INICIANDO PRUEBAS DEL MÓDULO DE RESERVAS")
    print("="*60)

    # 1. Creamos una clase hija temporal para poder instanciar un servicio
    class ServicioPrueba(Servicio):
        def calcular_costo(self):
            return self.get_precio_base() * 1.19
        def descripcion(self):
            return f"Servicio de prueba: {self.get_nombre()}"

    # 2. Preparamos los datos de prueba
    cliente_mock = "Reagon Ramirez" # Simulamos un cliente
    
    # Creamos un servicio disponible y uno NO disponible
    servicio_disponible = ServicioPrueba("Alquiler Video Beam", 50000)
    servicio_agotado = ServicioPrueba("Sala de Juntas VIP", 120000, disponible=False)

    # ---------------------------------------------------------
    # ESCENARIO 1: Reserva exitosa
    # ---------------------------------------------------------
    print("\n--- ESCENARIO 1: Creación y confirmación exitosa ---")
    try:
        reserva_exitosa = Reserva(cliente_mock, servicio_disponible, 4)
        reserva_exitosa.confirmar_reserva()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # ---------------------------------------------------------
    # ESCENARIO 2: Error de datos (Duración inválida)
    # ---------------------------------------------------------
    print("\n--- ESCENARIO 2: Fallo intencional por datos inválidos ---")
    try:
        # Intentamos enviar letras en lugar de números para la duración
        reserva_invalida = Reserva(cliente_mock, servicio_disponible, "ocho horas")
    except ReservaError as e:
        print(f"🛡️ Excepción capturada (El sistema no colapsó): {e}")

    # ---------------------------------------------------------
    # ESCENARIO 3: Error de disponibilidad
    # ---------------------------------------------------------
    print("\n--- ESCENARIO 3: Fallo intencional por servicio agotado ---")
    try:
        reserva_fallida = Reserva(cliente_mock, servicio_agotado, 2)
        reserva_fallida.confirmar_reserva()
    except DisponibilidadError as e:
        print(f"🛡️ Excepción capturada (El sistema no colapsó): {e}")

    # ---------------------------------------------------------
    # ESCENARIO 4: Error lógico (Cancelar algo ya cancelado)
    # ---------------------------------------------------------
    print("\n--- ESCENARIO 4: Fallo intencional en lógica de negocio ---")
    try:
        # Cancelamos la primera reserva con éxito
        reserva_exitosa.cancelar_reserva()
        # Intentamos cancelarla de nuevo para forzar el error
        reserva_exitosa.cancelar_reserva()
    except ReservaError as e:
        print(f"🛡️ Excepción capturada (El sistema no colapsó): {e}")

    print("\n" + "="*60)
    print("✅ PRUEBAS FINALIZADAS CON ÉXITO")
    print("El programa terminó su ejecución limpiamente. Revisa el archivo 'logs.txt'.")
    print("="*60)