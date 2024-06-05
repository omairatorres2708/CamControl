# Importa la clase Pin y I2C para control de pines GPIO
from machine import Pin, I2C
# Importa el módulo ssd1306 para controlar la pantalla OLED
import ssd1306

# Inicializa el objeto I2C en el bus I2C 0, usando el pin GPIO 17 para SCL y GPIO 23 para SDA
i2c = I2C(0, scl=Pin(17), sda=Pin(23))
# Define las dimensiones de la pantalla OLED en píxeles
Ancho = 128
Alto = 64
# Inicializa el objeto de la pantalla OLED con las dimensiones especificadas y el bus I2C configurado
oled = ssd1306.SSD1306_I2C(Ancho, Alto, i2c)

       
# Función para mostrar la frecuencia cardíaca y la temperatura en la pantalla OLED
def mostrar_frecuencia_temperatura(frecuencia, temperatura):
    oled.fill(0)  # Limpia la pantalla para prepararla para nuevos datos
    mensaje1 = "FC: {}".format(frecuencia)  # Prepara mensaje de frecuencia cardíaca
    mensaje2 = "Temp C: {}".format(temperatura)  # Prepara mensaje de temperatura
    oled.text(mensaje1, 0, 20)  # Muestra la frecuencia cardíaca en la pantalla
    oled.text(mensaje2, 0, 30)  # Muestra la temperatura en la pantalla
    oled.show()  # Actualiza la pantalla para mostrar los nuevos mensajes

# Función para mostrar instrucciones de configuración de alarma
def mostrar_mensaje():
    oled.fill(0)  # Limpia la pantalla completamente
    oled.text("Config. Alarma:", 0, 1)
    oled.text("Ingrese el", 0, 10)
    oled.text("tiempo (min).", 0, 20)
    oled.text("Finalice con A", 0, 30)
    oled.show()  # Actualiza la pantalla para mostrar el mensaje

# Función para mostrar un mensaje informativo en una posición específica
def mostrar_mensaje_info(mensaje):
    oled.fill(0)  # Limpia la pantalla para asegurar la visibilidad del mensaje
    oled.text(mensaje, 0, 50)  # Muestra el mensaje en la posición y=50
    oled.show()  # Actualiza la pantalla

# Función para mostrar el tiempo establecido en minutos
def mostrar_mensaje_dig(Digitos):
    oled.fill(0)  # Limpia la pantalla antes de mostrar nuevo contenido
    mensajeTiempo = "Tiempo: {} min".format(Digitos)
    oled.text(mensajeTiempo, 0, 40)  # Muestra el tiempo configurado en la pantalla
    oled.show()  # Actualiza la pantalla para visualizar el tiempo
    print(mensajeTiempo)  # Opcional: imprime el mensaje en la consola