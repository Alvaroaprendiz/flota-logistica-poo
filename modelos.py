# ==============================================================================
# modelos.py - SISTEMA DE CONTROL DE FLOTA PARA LOGÍSTICA URBANA (Avance 3)
# Alumno: Álvaro Joseph Ramírez Pulido
# Materia: Programación Orientada a Objetos
#
# Este módulo contiene SOLO la definición de las clases del sistema:
#   - Clases auxiliares para Composición: Conductor y Paquete
#   - Clase base: VehiculoLogistica (con Encapsulamiento)
#   - Subclase: MotoReparto (Herencia y Polimorfismo)
#
# Composición ("tiene-un"):
#   - Un VehiculoLogistica TIENE UN Conductor.
#   - Una MotoReparto TIENE UNA lista de objetos Paquete en su caja.
# ==============================================================================


# ------------------------------------------------------------------------------
# Clase auxiliar para Composición: Conductor
# ------------------------------------------------------------------------------
class Conductor:

    def __init__(self, nombre, licencia, calificacion=5.0):
        self.nombre = nombre
        self.licencia = licencia
        self.calificacion = calificacion
        self.viajes_realizados = 0

    def registrar_viaje(self):
        self.viajes_realizados += 1

    def presentarse(self):
        return (f"{self.nombre} (licencia {self.licencia}, "
                f"calificación {self.calificacion}, viajes: {self.viajes_realizados})")


# ------------------------------------------------------------------------------
# Clase auxiliar para Composición: Paquete
# ------------------------------------------------------------------------------
class Paquete:

    def __init__(self, guia, destino, peso_kg):
        if peso_kg <= 0:
            raise ValueError("El peso del paquete debe ser mayor a 0.")
        self.guia = guia
        self.destino = destino
        self.peso_kg = peso_kg

    def etiqueta(self):
        return f"[{self.guia}] {self.peso_kg} kg -> {self.destino}"


# ------------------------------------------------------------------------------
# Creación de la clase base (superclase)
# ------------------------------------------------------------------------------
class VehiculoLogistica:

    # Cada cuántos kilómetros le toca servicio a un vehículo normal
    INTERVALO_SERVICIO_KM = 10000

    def __init__(self, marca_modelo, anio, kilometraje_inicial, conductor, en_servicio=True):
        self.marca_modelo = marca_modelo
        self.anio = anio
        self.entregas_completadas = 0
        self.en_servicio = en_servicio

        # COMPOSICIÓN: el vehículo "tiene-un" Conductor
        self.conductor = conductor

        # Aplicación de Encapsulamiento: kilometraje privado, se asigna por el setter
        self.__kilometraje = 0
        self.kilometraje = kilometraje_inicial

    # --- Aplicación de Encapsulamiento: getter con @property ---
    @property
    def kilometraje(self):
        return self.__kilometraje

    # --- Aplicación de Encapsulamiento: setter con validación ---
    @kilometraje.setter
    def kilometraje(self, nuevo_km):
        if nuevo_km < 0:
            raise ValueError("El kilometraje no puede ser negativo.")
        if nuevo_km < self.__kilometraje:
            raise ValueError(
                f"El kilometraje no puede bajar de {self.__kilometraje} km a {nuevo_km} km."
            )
        self.__kilometraje = nuevo_km

    # --- Composición: cambiar el conductor asignado ---
    def asignar_conductor(self, nuevo_conductor):
        anterior = self.conductor.nombre
        self.conductor = nuevo_conductor
        print(f"El {self.marca_modelo} cambió de conductor: {anterior} -> {nuevo_conductor.nombre}.")

    # Método 1: registra una entrega y actualiza los contadores
    def registrar_entrega(self, distancia_km):
        if self.en_servicio:
            self.kilometraje += distancia_km          # pasa por el setter
            self.entregas_completadas += 1
            self.conductor.registrar_viaje()          # delegación al objeto contenido
            print(f"Entrega exitosa en el {self.marca_modelo} con {self.conductor.nombre}. "
                  f"Recorridos: {distancia_km} km. Total histórico: {self.entregas_completadas} entregas.")
        else:
            print(f"Operación denegada: El {self.marca_modelo} ({self.anio}) está fuera de servicio.")

    # Método 2: cambia el estado del vehículo
    def cambiar_estado(self, estado):
        self.en_servicio = estado
        estado_str = "Activo en plataforma" if self.en_servicio else "Inactivo / En taller"
        print(f"Actualización: El estado del {self.marca_modelo} ha cambiado a '{estado_str}'.")

    # Método 3: revisa si ya le toca mantenimiento (se sobrescribe en la subclase)
    def evaluar_mantenimiento(self):
        km_desde_ultimo_servicio = self.kilometraje % self.INTERVALO_SERVICIO_KM
        if km_desde_ultimo_servicio > self.INTERVALO_SERVICIO_KM - 500:
            print(f"ALERTA PREVENTIVA: El {self.marca_modelo} tiene {self.kilometraje} km. "
                  f"Agendar mantenimiento pronto.")
        else:
            print(f"El {self.marca_modelo} no requiere mantenimiento urgente por kilometraje.")

    # Método 4: muestra todos los datos (se extiende en la subclase)
    def mostrar_info(self):
        estado_str = "Disponible" if self.en_servicio else "No disponible"
        print(f"\n--- REPORTE DE UNIDAD: {self.marca_modelo.upper()} ---")
        print(f"  Año: {self.anio}")
        print(f"  Odómetro: {self.kilometraje} km")
        print(f"  Rendimiento: {self.entregas_completadas} entregas completadas")
        print(f"  Estatus actual: {estado_str}")
        # Composición: se delega en el método del objeto Conductor
        print(f"  Conductor: {self.conductor.presentarse()}")


# ------------------------------------------------------------------------------
# Uso de super() y Herencia: clase derivada (subclase)
# ------------------------------------------------------------------------------
class MotoReparto(VehiculoLogistica):

    def __init__(self, marca_modelo, anio, kilometraje_inicial, conductor,
                 cilindrada_cc, capacidad_caja_kg, en_servicio=True):
        # super() reutiliza el constructor de VehiculoLogistica
        super().__init__(marca_modelo, anio, kilometraje_inicial, conductor, en_servicio)
        self.cilindrada_cc = cilindrada_cc
        self.capacidad_caja_kg = capacidad_caja_kg

        # COMPOSICIÓN: la moto "tiene-una" lista de objetos Paquete (atributo protegido)
        self._paquetes = []

    # Peso total: se calcula sumando el peso de cada objeto Paquete contenido
    @property
    def carga_actual_kg(self):
        return sum(p.peso_kg for p in self._paquetes)

    # Método 5: carga un objeto Paquete sin pasar la capacidad de la caja
    def cargar_paquete(self, paquete):
        if self.carga_actual_kg + paquete.peso_kg > self.capacidad_caja_kg:
            libre = self.capacidad_caja_kg - self.carga_actual_kg
            print(f"Paquete rechazado {paquete.etiqueta()}: no cabe en la {self.marca_modelo}. "
                  f"Espacio libre: {libre} kg.")
        else:
            self._paquetes.append(paquete)
            print(f"Cargado {paquete.etiqueta()} en la {self.marca_modelo}. "
                  f"Carga actual: {self.carga_actual_kg}/{self.capacidad_caja_kg} kg.")

    # Método 6: entrega el primer paquete de la caja (delega en registrar_entrega y en Paquete)
    def entregar_siguiente(self, distancia_km):
        if not self._paquetes:
            print(f"La {self.marca_modelo} no tiene paquetes por entregar.")
            return
        paquete = self._paquetes.pop(0)
        print(f"Entregando {paquete.etiqueta()}...")
        self.registrar_entrega(distancia_km)

    # --- Sobrescritura de métodos (Polimorfismo): servicio cada 4,000 km ---
    def evaluar_mantenimiento(self):
        intervalo = 4000
        km_desde_ultimo_servicio = self.kilometraje % intervalo
        if km_desde_ultimo_servicio > intervalo - 300:
            print(f"ALERTA MOTO: La {self.marca_modelo} ({self.cilindrada_cc} cc) tiene "
                  f"{self.kilometraje} km. Toca cambio de aceite y revisión de cadena.")
        else:
            faltan = intervalo - km_desde_ultimo_servicio
            print(f"La {self.marca_modelo} está al corriente. Faltan {faltan:.1f} km para su servicio.")

    # --- Sobrescritura de métodos (Polimorfismo): extiende el reporte del padre ---
    def mostrar_info(self):
        super().mostrar_info()
        print(f"  Tipo: Motocicleta de reparto ({self.cilindrada_cc} cc)")
        print(f"  Caja: {self.carga_actual_kg}/{self.capacidad_caja_kg} kg ocupados")
        for paquete in self._paquetes:
            print(f"    - {paquete.etiqueta()}")
