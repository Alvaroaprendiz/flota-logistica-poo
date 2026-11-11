# ==============================================================================
# SISTEMA DE CONTROL DE FLOTA PARA LOGÍSTICA URBANA  -  Avance 2
# Alumno: Álvaro Joseph Ramírez Pulido
# Materia: Programación Orientada a Objetos
#
# Descripción del sistema:
# Modela los vehículos que trabajan en plataformas de entrega a domicilio.
# Cada unidad lleva su propio kilometraje, entregas completadas y estado de
# servicio. En este avance se amplía la clase VehiculoLogistica del Avance 1:
#   - Encapsulamiento: el kilometraje ahora es privado y se controla con @property.
#   - Herencia: se agrega la subclase MotoReparto, que hereda de VehiculoLogistica.
#   - Polimorfismo: MotoReparto sobrescribe evaluar_mantenimiento() y mostrar_info().
# ==============================================================================


# ------------------------------------------------------------------------------
# Creación de la clase base (superclase)
# ------------------------------------------------------------------------------
class VehiculoLogistica:

    # Cada cuántos kilómetros le toca servicio a un vehículo normal
    INTERVALO_SERVICIO_KM = 10000

    def __init__(self, marca_modelo, anio, kilometraje_inicial, en_servicio=True):
        self.marca_modelo = marca_modelo
        self.anio = anio
        self.entregas_completadas = 0
        self.en_servicio = en_servicio

        # Aplicación de Encapsulamiento:
        # el kilometraje es PRIVADO (doble guion bajo). Nadie lo puede cambiar
        # directo desde afuera; se asigna pasando por el setter para validarlo.
        self.__kilometraje = 0
        self.kilometraje = kilometraje_inicial

    # --- Aplicación de Encapsulamiento: getter con @property ---
    @property
    def kilometraje(self):
        return self.__kilometraje

    # --- Aplicación de Encapsulamiento: setter con validación ---
    @kilometraje.setter
    def kilometraje(self, nuevo_km):
        # Un odómetro no puede ser negativo ni regresarse
        if nuevo_km < 0:
            raise ValueError("El kilometraje no puede ser negativo.")
        if nuevo_km < self.__kilometraje:
            raise ValueError(
                f"El kilometraje no puede bajar de {self.__kilometraje} km a {nuevo_km} km."
            )
        self.__kilometraje = nuevo_km

    # Método 1: registra una entrega y actualiza los contadores
    def registrar_entrega(self, distancia_km):
        if self.en_servicio:
            self.kilometraje += distancia_km          # pasa por el setter
            self.entregas_completadas += 1
            print(f"Entrega exitosa en el {self.marca_modelo}. Recorridos: {distancia_km} km. "
                  f"Total histórico: {self.entregas_completadas} entregas.")
        else:
            print(f"Operación denegada: El {self.marca_modelo} ({self.anio}) está fuera de servicio.")

    # Método 2: cambia el estado del vehículo
    def cambiar_estado(self, estado):
        self.en_servicio = estado
        estado_str = "Activo en plataforma" if self.en_servicio else "Inactivo / En taller"
        print(f"Actualización: El estado del {self.marca_modelo} ha cambiado a '{estado_str}'.")

    # Método 3: revisa si ya le toca mantenimiento (será sobrescrito en la subclase)
    def evaluar_mantenimiento(self):
        km_desde_ultimo_servicio = self.kilometraje % self.INTERVALO_SERVICIO_KM
        if km_desde_ultimo_servicio > self.INTERVALO_SERVICIO_KM - 500:
            print(f"ALERTA PREVENTIVA: El {self.marca_modelo} tiene {self.kilometraje} km. "
                  f"Agendar mantenimiento pronto.")
        else:
            print(f"El {self.marca_modelo} no requiere mantenimiento urgente por kilometraje.")

    # Método 4: muestra todos los datos (será extendido en la subclase)
    def mostrar_info(self):
        estado_str = "Disponible" if self.en_servicio else "No disponible"
        print(f"\n--- REPORTE DE UNIDAD: {self.marca_modelo.upper()} ---")
        print(f"  Año: {self.anio}")
        print(f"  Odómetro: {self.kilometraje} km")
        print(f"  Rendimiento: {self.entregas_completadas} entregas completadas")
        print(f"  Estatus actual: {estado_str}")


# ------------------------------------------------------------------------------
# Uso de super() y Herencia: clase derivada (subclase)
# ------------------------------------------------------------------------------
class MotoReparto(VehiculoLogistica):

    def __init__(self, marca_modelo, anio, kilometraje_inicial, cilindrada_cc,
                 capacidad_caja_kg, en_servicio=True):
        # super() llama al constructor de VehiculoLogistica para reutilizar
        # sus atributos (marca_modelo, anio, kilometraje, en_servicio)
        super().__init__(marca_modelo, anio, kilometraje_inicial, en_servicio)

        # Dos atributos nuevos, propios de la subclase
        self.cilindrada_cc = cilindrada_cc
        self.capacidad_caja_kg = capacidad_caja_kg

        # Atributo protegido (un guion bajo): carga que lleva la caja en este momento
        self._carga_actual_kg = 0

    # Método 5 (propio de la subclase): cargar un paquete sin pasar la capacidad
    def cargar_paquete(self, peso_kg):
        if peso_kg <= 0:
            print(f"Peso inválido: {peso_kg} kg.")
        elif self._carga_actual_kg + peso_kg > self.capacidad_caja_kg:
            libre = self.capacidad_caja_kg - self._carga_actual_kg
            print(f"Paquete rechazado: {peso_kg} kg no caben en la {self.marca_modelo}. "
                  f"Espacio libre: {libre} kg.")
        else:
            self._carga_actual_kg += peso_kg
            print(f"Paquete de {peso_kg} kg cargado en la {self.marca_modelo}. "
                  f"Carga actual: {self._carga_actual_kg}/{self.capacidad_caja_kg} kg.")

    # --- Sobrescritura de métodos (Polimorfismo) ---
    # Una moto necesita servicio más seguido que un auto: cada 4,000 km.
    def evaluar_mantenimiento(self):
        intervalo = 4000
        km_desde_ultimo_servicio = self.kilometraje % intervalo
        if km_desde_ultimo_servicio > intervalo - 300:
            print(f"ALERTA MOTO: La {self.marca_modelo} ({self.cilindrada_cc} cc) tiene "
                  f"{self.kilometraje} km. Toca cambio de aceite y revisión de cadena.")
        else:
            faltan = intervalo - km_desde_ultimo_servicio
            print(f"La {self.marca_modelo} está al corriente. Faltan {faltan:.1f} km para su servicio.")

    # --- Sobrescritura de métodos (Polimorfismo) ---
    # Reutiliza el reporte del padre con super() y le agrega los datos de la moto.
    def mostrar_info(self):
        super().mostrar_info()
        print(f"  Tipo: Motocicleta de reparto ({self.cilindrada_cc} cc)")
        print(f"  Caja: {self._carga_actual_kg}/{self.capacidad_caja_kg} kg ocupados")


# ==============================================================================
# Instanciación y pruebas
# ==============================================================================
if __name__ == "__main__":

    # 3 objetos distintos: 1 de la clase base y 2 de la subclase
    vagoneta = VehiculoLogistica("Ford Focus Wagon", 2002, 185000)
    moto1 = MotoReparto("Honda Cargo 150", 2023, 14200, cilindrada_cc=150, capacidad_caja_kg=20)
    moto2 = MotoReparto("Italika FT 125", 2021, 7750, cilindrada_cc=125, capacidad_caja_kg=15)

    print("\n=== 1. ENCAPSULAMIENTO ===")
    # Getter: se consulta como si fuera un atributo normal
    print(f"Kilometraje de la vagoneta (getter): {vagoneta.kilometraje} km")
    # Setter con valor válido
    vagoneta.kilometraje = 185200
    print(f"Kilometraje actualizado (setter): {vagoneta.kilometraje} km")
    # Setter con valores inválidos: la validación los rechaza
    try:
        vagoneta.kilometraje = -50
    except ValueError as error:
        print(f"Rechazado por el setter: {error}")
    try:
        vagoneta.kilometraje = 1000
    except ValueError as error:
        print(f"Rechazado por el setter: {error}")
    # El atributo privado no se puede leer directo desde afuera
    try:
        print(vagoneta.__kilometraje)
    except AttributeError:
        print("No se puede leer vagoneta.__kilometraje directo: es privado.")

    print("\n=== 2. HERENCIA ===")
    # La moto usa métodos que NO escribimos en MotoReparto: los heredó del padre
    moto1.registrar_entrega(3.2)
    moto1.cambiar_estado(False)
    moto1.registrar_entrega(5.0)
    moto1.cambiar_estado(True)
    # Método propio de la subclase
    moto1.cargar_paquete(12)
    moto1.cargar_paquete(10)
    print(f"¿moto1 es un VehiculoLogistica? {isinstance(moto1, VehiculoLogistica)}")

    print("\n=== 3. POLIMORFISMO (método sobrescrito) ===")
    # El mismo mensaje, evaluar_mantenimiento(), responde distinto según la clase
    moto2.registrar_entrega(6.5)
    flota = [vagoneta, moto1, moto2]
    for unidad in flota:
        unidad.evaluar_mantenimiento()

    print("\n=== 4. INDEPENDENCIA DE DATOS ENTRE INSTANCIAS (self) ===")
    vagoneta.registrar_entrega(12.5)
    vagoneta.registrar_entrega(8.0)
    print(f"Entregas -> vagoneta: {vagoneta.entregas_completadas} | "
          f"moto1: {moto1.entregas_completadas} | moto2: {moto2.entregas_completadas}")

    print("\n=== 5. REPORTE FINAL ===")
    for unidad in flota:
        unidad.mostrar_info()
    print("-" * 40)
