# Importa la clase Pin y PWM para control de pines GPIO
from machine import Pin, PWM

# Configura el pin GPIO 13 como salida para el zumbador
pin_zumbador = Pin(13, Pin.OUT)  

# Configura el pin GPIO 15 como entrada con resistencia de pull-up
pin_encendido = Pin(15, Pin.IN, Pin.PULL_UP)  

def encender_zumbador(timer):
    # Activa el pin del zumbador, enviando corriente para que suene
    pin_zumbador.on()
    
def apagar_zumbador():
    # Desactiva el pin del zumbador, cortando la corriente para que deje de sonar
    pin_zumbador.off()
