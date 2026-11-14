# ==============================================================================
# main.py - SISTEMA DE CONTROL DE FLOTA PARA LOGÍSTICA URBANA (Avance 3)
# Alumno: Álvaro Joseph Ramírez Pulido
#
# Archivo principal de ejecución. Solo contiene:
#   1. Las importaciones desde el módulo modelos.py
#   2. La instanciación de los objetos
#   3. Las pruebas de Encapsulamiento, Herencia, Polimorfismo y Composición
# ==============================================================================

# Importaciones: las clases viven en el módulo modelos.py
from modelos import Conductor, Paquete, VehiculoLogistica, MotoReparto


# ------------------------------------------------------------------------------
# Instanciación de objetos
# ------------------------------------------------------------------------------
# Objetos auxiliares (las "partes" de la composición)
luis = Conductor("Luis Hernández", "B-458213", 4.8)
ana = Conductor("Ana Torres", "A-102944", 4.9)
carlos = Conductor("Carlos Ruiz", "A-339871", 4.6)
maria = Conductor("María López", "B-770512", 4.7)

# Objetos principales: 1 de la clase base y 2 de la subclase
# Cada vehículo recibe su propio objeto Conductor (composición)
vagoneta = VehiculoLogistica("Ford Focus Wagon", 2002, 185000, luis)
moto1 = MotoReparto("Honda Cargo 150", 2023, 14200, ana, cilindrada_cc=150, capacidad_caja_kg=20)
moto2 = MotoReparto("Italika FT 125", 2021, 7750, carlos, cilindrada_cc=125, capacidad_caja_kg=15)


print("\n=== 1. COMPOSICIÓN (relación 'tiene-un') ===")
# El vehículo contiene un objeto Conductor; se usa su método a través del vehículo
print(f"Conductor de la vagoneta: {vagoneta.conductor.presentarse()}")
# La moto contiene objetos Paquete
moto1.cargar_paquete(Paquete("GDL-001", "Col. Americana", 8))
moto1.cargar_paquete(Paquete("GDL-002", "Chapultepec", 6))
moto1.cargar_paquete(Paquete("GDL-003", "Providencia", 9))   # rebota: no cabe
# Entregar un paquete actualiza la moto Y el conductor contenido (delegación)
moto1.entregar_siguiente(3.2)
print(f"Viajes de Ana después de la entrega: {ana.viajes_realizados}")
# Cambiar la parte sin cambiar el contenedor: la vagoneta ahora la maneja María
vagoneta.asignar_conductor(maria)
vagoneta.registrar_entrega(12.5)


print("\n=== 2. ENCAPSULAMIENTO ===")
print(f"Kilometraje de la vagoneta (getter): {vagoneta.kilometraje} km")
vagoneta.kilometraje = 185200
print(f"Kilometraje actualizado (setter): {vagoneta.kilometraje} km")
for valor in (-50, 1000):
    try:
        vagoneta.kilometraje = valor
    except ValueError as error:
        print(f"Rechazado por el setter: {error}")
try:
    print(vagoneta.__kilometraje)
except AttributeError:
    print("No se puede leer vagoneta.__kilometraje directo: es privado.")


print("\n=== 3. HERENCIA ===")
# Métodos heredados de VehiculoLogistica, usados por una MotoReparto
moto2.cambiar_estado(False)
moto2.registrar_entrega(5.0)
moto2.cambiar_estado(True)
moto2.registrar_entrega(6.5)
print(f"¿moto2 es un VehiculoLogistica? {isinstance(moto2, VehiculoLogistica)}")


print("\n=== 4. POLIMORFISMO (método sobrescrito) ===")
flota = [vagoneta, moto1, moto2]
for unidad in flota:
    unidad.evaluar_mantenimiento()


print("\n=== 5. REPORTE FINAL ===")
for unidad in flota:
    unidad.mostrar_info()
print("-" * 40)
