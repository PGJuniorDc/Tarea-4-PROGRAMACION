"""
excepciones.py

Módulo encargado de centralizar el manejo de errores personalizados
y el registro (logging) de eventos en archivos de texto plano.
Cumple con los principios de herencia y encapsulación.
"""

import datetime

# =========================================================
# JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# =========================================================

class SoftwareFJError(Exception):
    """
    Clase base para todas las excepciones del proyecto Software FJ.
    Hereda de la clase base Exception de Python.
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje


class ClienteError(SoftwareFJError):
    """
    Excepción lanzada cuando hay errores relacionados con la
    creación, validación o gestión de los clientes.
    """
    pass


class ReservaError(SoftwareFJError):
    """
    Excepción lanzada cuando ocurre un error en el proceso
    de creación, modificación o cancelación de una reserva.
    """
    pass


class DisponibilidadError(SoftwareFJError):
    """
    Excepción lanzada cuando se intenta reservar un servicio
    que no está disponible o cuyo cupo/stock se ha agotado.
    """
    pass


# =========================================================
# GESTIÓN DE LOGS (REGISTRO DE ERRORES)
# =========================================================

class GestorLogs:
    """
    Clase utilitaria para manejar la escritura de errores en el archivo logs.txt.
    No requiere ser instanciada (usa métodos estáticos).
    """
    
    # Nombre del archivo definido como constante a nivel de clase
    ARCHIVO_LOGS = "logs.txt"

    @staticmethod
    def registrar_error(tipo_error, mensaje_error, contexto="General"):
        """
        Escribe el detalle de un error en el archivo de texto plano.
        
        Args:
            tipo_error (str): El nombre de la clase de excepción (ej. 'ReservaError').
            mensaje_error (str): El detalle del fallo.
            contexto (str): En qué parte del código ocurrió (ej. 'Clase Reserva - método confirmar').
        """
        # Obtenemos la fecha y hora exacta del momento del error
        ahora = datetime.datetime.now()
        marca_tiempo = ahora.strftime("%Y-%m-%d %H:%M:%S")
        
        # Formateamos el mensaje que irá en el archivo
        linea_log = f"[{marca_tiempo}] | TIPO: {tipo_error} | CONTEXTO: {contexto} | DETALLE: {mensaje_error}\n"
        
        # Usamos el bloque 'with' para abrir el archivo en modo 'a' (append/añadir).
        # Esto asegura que el archivo se cierre correctamente incluso si algo falla,
        # y no sobrescribe el historial anterior.
        try:
            with open(GestorLogs.ARCHIVO_LOGS, mode="a", encoding="utf-8") as archivo:
                archivo.write(linea_log)
        except Exception as e:
            # En caso extremo de que falle la escritura del log (ej. permisos de sistema),
            # lo mostramos por consola para no perder la información.
            print(f"Fallo crítico al intentar escribir en logs.txt: {e}")