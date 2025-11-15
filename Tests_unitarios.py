
import math

class Sensortemperatura:
    """
    Wrapper ligero para parsear líneas que traen temperatura y humedad.
    Formatos soportados (según tu protocolo):
      - "1:<temp>:<hum>"
      - "1:<temp>:<hum>:A:<avg>"  (se ignora A:avg aquí)
    Método parse_line devuelve (temp: float, hum: float)
    """
    @staticmethod
    def parse_line(line: str):
        if not line:
            raise ValueError("Empty line")
        trozos = line.strip().split(':')
        # aceptamos formatos que empiezan por '1'
        if len(trozos) < 3 or trozos[0] != '1':
            raise ValueError(f"Formato inválido: {line!r}")
        try:
            temp = float(trozos[1])
            hum = float(trozos[2])
        except Exception as e:
            raise ValueError(f"Valores no numéricos en: {line!r}") from e
        return temp, hum


class Servo:
    """
    Wrapper para controlar un servo. Recibe un objeto 'driver' con método set_angle(angle)
    en el que delega la operación física. Este driver será mockeado en tests.
    """
    def __init__(self, driver):
        self._driver = driver

    def set_angle(self, angle: int):
        # normalizar/clamp 0..180
        if angle is None:
            raise ValueError("Angle required")
        a = int(angle)
        if a < 0:
            a = 0
        if a > 180:
            a = 180
        # delegar al driver (p.e. PWM)
        self._driver.set_angle(a)
        return a  # devuelvo el ángulo efectivo para facilitar test


class Ultrasonidos:
    """
    Wrapper para cálculo de distancia. La medición real depende de un método
    pulse_duration_us() que devuelve la duración del eco en microsegundos
    o 0 en caso de timeout.
    """
    SPEED_CM_PER_US = 0.034 / 2.0  # cm por microsegundo dividido entre 2 (ida+vuelta)

    def __init__(self, pulse_provider):
        """
        pulse_provider debe ser un objeto con método pulse_duration_us() -> int
        (microsegundos), o una función.
        """
        self._provider = pulse_provider

    def distance_from_duration(self, duration_us: int):
        """Convierte duración (microsegundos) en distancia (cm)."""
        if duration_us <= 0:
            return -1.0
        return duration_us * UltrasonicSensor.SPEED_CM_PER_US

    def measure(self):
        """
        Llama a provider.pulse_duration_us() y devuelve distancia en cm o -1 si fallo.
        """
        d = None
        if callable(self._provider):
            d = self._provider()
        else:
            d = self._provider.pulse_duration_us()
        if d is None or d <= 0:
            return -1.0
        return self.distance_from_duration(d)
