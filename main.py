"""
main.py

Sistema principal de Software FJ.

Integra:
- Clientes
- Servicios
- Reservas
- Manejo de excepciones
- Polimorfismo
- Herencia
- Registro de errores
"""

from cliente import Cliente, ClienteError

from servicios_especificos import (
    ReservaSala,
    AlquilerEquipo,
    Asesoria
)

from reserva import Reserva

from servicio import ServicioError

from excepciones import (
    ReservaError,
    DisponibilidadError,
    GestorLogs
)


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def main():

    print("\n" + "=" * 70)
    print("🚀 SISTEMA INTEGRAL SOFTWARE FJ")
    print("=" * 70)

    # =====================================================
    # LISTAS DEL SISTEMA
    # =====================================================

    clientes = []
    servicios = []
    reservas = []

    # =====================================================
    # CASO 1 - CREACIÓN DE CLIENTES
    # =====================================================

    print("\n===== CREACIÓN DE CLIENTES =====")

    try:

        cliente1 = Cliente(
            "Daniel Castellanos",
            "daniel@gmail.com",
            "3201234567",
            "123456789"
        )

        cliente2 = Cliente(
            "Laura Martinez",
            "laura@gmail.com",
            "3009876543",
            "987654321"
        )

        clientes.append(cliente1)
        clientes.append(cliente2)

        print("\n✓ Clientes creados correctamente")

        for cliente in clientes:
            print(cliente.mostrar_informacion())

    except ClienteError as error:

        GestorLogs.registrar_error(
            "ClienteError",
            str(error),
            "main.py - creación clientes"
        )

        print(f"❌ Error en cliente: {error}")

    # =====================================================
    # CASO 2 - CREACIÓN DE SERVICIOS
    # =====================================================

    print("\n===== CREACIÓN DE SERVICIOS =====")

    try:

        sala = ReservaSala(
            "Sala Ejecutiva",
            80000,
            15
        )

        equipo = AlquilerEquipo(
            "Portátil HP",
            50000,
            "Laptop"
        )

        asesoria = Asesoria(
            "Consultoría Python",
            120000,
            "Programación"
        )

        servicios.extend([
            sala,
            equipo,
            asesoria
        ])

        print("\n✓ Servicios creados correctamente")

        # POLIMORFISMO
        for servicio in servicios:

            print(servicio.mostrar_informacion_base())

            print("Descripción:")
            print(servicio.descripcion())

    except ServicioError as error:

        GestorLogs.registrar_error(
            "ServicioError",
            str(error),
            "main.py - creación servicios"
        )

        print(f"❌ Error en servicio: {error}")

    # =====================================================
    # CASO 3 - CREACIÓN DE RESERVAS
    # =====================================================

    print("\n===== CREACIÓN DE RESERVAS =====")

    try:

        reserva1 = Reserva(
            cliente1,
            sala,
            3
        )

        reserva2 = Reserva(
            cliente2,
            equipo,
            5
        )

        reservas.extend([
            reserva1,
            reserva2
        ])

        print("\n✓ Reservas creadas correctamente")

    except ReservaError as error:

        GestorLogs.registrar_error(
            "ReservaError",
            str(error),
            "main.py - creación reservas"
        )

        print(f"❌ Error en reserva: {error}")

    # =====================================================
    # CASO 4 - CONFIRMACIÓN DE RESERVAS
    # =====================================================

    print("\n===== CONFIRMACIÓN DE RESERVAS =====")

    for reserva in reservas:

        try:

            reserva.confirmar_reserva()

        except DisponibilidadError as error:

            print(f"❌ Disponibilidad: {error}")

        except ReservaError as error:

            print(f"❌ Reserva: {error}")

    # =====================================================
    # CASO 5 - CANCELACIÓN
    # =====================================================

    print("\n===== CANCELACIÓN DE RESERVA =====")

    try:

        reserva1.cancelar_reserva()

    except ReservaError as error:

        print(f"❌ Error cancelando: {error}")

    # =====================================================
    # CASO 6 - ERROR CONTROLADO
    # =====================================================

    print("\n===== ERROR INTENCIONAL =====")

    try:

        cliente_error = Cliente(
            "",
            "correo_malo",
            "abc",
            "12"
        )

    except ClienteError as error:

        GestorLogs.registrar_error(
            "ClienteError",
            str(error),
            "main.py - error intencional"
        )

        print(f"🛡️ Excepción capturada: {error}")

    # =====================================================
    # CASO 7 - SERVICIO NO DISPONIBLE
    # =====================================================

    print("\n===== SERVICIO NO DISPONIBLE =====")

    try:

        sala_ocupada = ReservaSala(
            "Sala VIP",
            200000,
            25,
            disponible=False
        )

        reserva_fallida = Reserva(
            cliente1,
            sala_ocupada,
            2
        )

        reserva_fallida.confirmar_reserva()

    except DisponibilidadError as error:

        print(f"🛡️ Excepción capturada: {error}")

    # =====================================================
    # FINAL DEL SISTEMA
    # =====================================================

    print("\n" + "=" * 70)
    print("✅ SISTEMA FINALIZADO CORRECTAMENTE")
    print("Revisar logs.txt para verificar registros.")
    print("=" * 70)


# =========================================================
# EJECUCIÓN PRINCIPAL
# =========================================================

if __name__ == "__main__":

    main()