# Importa la clase Pin y PWM para control de pines GPIO
from machine import Pin, PWM

#Variables

servo1 = PWM(Pin(25), freq=50)  # El servo1 es el que controla la elevacion de espalda.
servo2 = PWM(Pin(32), freq=50)  # El servo2 es el que controla la inclinacion de las piernas.
servo3 = PWM(Pin(19), freq=50)  # El servo3 es el que controla el ajuste de altura.
servo4 = PWM(Pin(15), freq=50)  # El servo4 es el que controla el ajuste de altura.

# Diccionario para mantener el ángulo de los servos
angulos_Servos = {
    "angulo_servo_1":0,
    "angulo_servo_2":0,
    "angulo_servo_3_4":90
}

# Metodo que configura el angulo del servo que se envie por parametros.
#servo = servo que se quiere mover.
#angulo = Angulo nuevo del servo que se quiere asignar.
def configurar_angulo(servo, angulo):
    min_duty = 26  # Valor de duty para 0 grados
    max_duty = 123  # Valor de duty para 180 grados
    duty = min_duty + (max_duty - min_duty) * angulo / 180
    servo.duty(int(duty))

# Metodo que configura la altura de la camilla.
# angulo = Angulo nuevo del servo que se quiere asignar.
def configuracion_Altura(add_Angulo):
    global servo3
    global servo4
    # Obtiene el ángulo actual compartido por los servomotores 3 y 4 desde un diccionario global.
    angulo_servo_3_4 = angulos_Servos['angulo_servo_3_4']
    
    # Incrementa el ángulo actual por un valor proporcionado por el parámetro add_Angulo.
    angulo_servo_3_4 = angulo_servo_3_4 + add_Angulo
    
    # Verifica si el nuevo ángulo está dentro de un rango permitido (0 a 100 grados).
    if angulo_servo_3_4 > 100 or angulo_servo_3_4 < 0:
        # Si el ángulo es mayor a 100 o menor a 0, imprime un mensaje de error.
        print("El servo 3 y 4 llego a su tope maximo o minimo.")
    else:
        # Si el ángulo está dentro del rango, configura ambos servos al nuevo ángulo.
        configurar_angulo(servo4, angulo_servo_3_4)
        configurar_angulo(servo3, angulo_servo_3_4)
        
        # Actualiza el ángulo en el diccionario global.
        angulos_Servos['angulo_servo_3_4'] = angulo_servo_3_4
        
        # Imprime el ángulo configurado.
        print("Angulo del servo 3 y 4: " + str(angulo_servo_3_4))

# Metodo que configura el espaldar de la camilla.
# servo1 = servo que se quiere mover.
# angulo = Angulo nuevo del servo que se quiere asignar.
def configuracion_espaldar(add_Angulo):
    global servo1
    # Obtiene el ángulo actual del servo1 desde un diccionario global de ángulos.
    angulo_servo1 = angulos_Servos['angulo_servo_1']
    
    # Ajusta el ángulo actual sumando el valor adicional proporcionado.
    angulo_servo1 = angulo_servo1 + add_Angulo
    
    # Verifica si el nuevo ángulo está dentro del rango operativo permitido para el servo1 (0 a 60 grados).
    if angulo_servo1 > 60 or angulo_servo1 < 0:
        # Si el ángulo excede los límites, imprime un mensaje de error.
        print("El servo 1 llego a su tope maximo o minimo.")
    else:
        # Si el ángulo es válido, configura el servo1 al nuevo ángulo.
        configurar_angulo(servo1, angulo_servo1)
        
        # Actualiza el ángulo en el diccionario global para mantener el estado.
        angulos_Servos['angulo_servo_1'] = angulo_servo1
        
        # Imprime el ángulo configurado para informar al usuario.
        print("Angulo del servo 1: " + str(angulo_servo1))

# Metodo que configura el espaldar de la camilla.
# servo2 = servo que se quiere mover.
# angulo = Angulo nuevo del servo que se quiere asignar.      
def configuracion_piernas(add_Angulo):
    global servo2
    # Obtiene el ángulo actual del servo2 desde un diccionario global.
    angulo_servo2 = angulos_Servos['angulo_servo_2']
    
    # Incrementa el ángulo actual por el valor adicional proporcionado.
    angulo_servo2 = angulo_servo2 + add_Angulo
    
    # Verifica si el nuevo ángulo está dentro del rango permitido (0 a 70 grados).
    if angulo_servo2 > 70 or angulo_servo2 < 0:
        # Si el ángulo es mayor a 70 o menor que 0, imprime un mensaje de error.
        print("El servo 2 llego a su tope maximo o minimo.")
    else:
        # Si el ángulo es válido, configura el servo2 al nuevo ángulo.
        configurar_angulo(servo2, angulo_servo2)
        
        # Actualiza el ángulo en el diccionario global.
        angulos_Servos['angulo_servo_2'] = angulo_servo2
        
        # Imprime el ángulo configurado para informar al usuario.
        print("Angulo del servo 2: " + str(angulo_servo2))
