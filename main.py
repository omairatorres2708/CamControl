
from machine import Timer
# Importa la libreria del teclado
import Teclado
# Importa la libreria pantalla para mostrar mensajes
import Pantalla
# Importa la libreria que controla el zumbador
import Alarma
# Importa la libreria que controla los servos.
import Servos
#Importa la libreria de BLE
from BLE import BLEUART
#Importar el módulo para el bluetooth
import bluetooth
# Importa el modulo de lecturas de temperatura y fecuencia.
import Lectures


#Variables
Nombre_Bluetooth = "CamControl"
PosicionServo = 10 #Velocidad con los que se mueven los servos
Estado_glo = 0; #Tipos de estados 0 = Mostrar Frecuencias, 1 = Configuracion de alarmas
Tiempo_Alerta_glo = ""; #Tiempo de alerta se espera el valor en minutos.
Tiempo_Temperatura = 10000 # El tiempo de temperatura esta en milisegundos
temporizador = Timer(0) # Temporizador de la alarma.
temporizador_Frec_Temp = Timer(1)

print(Nombre_Bluetooth, " Nombre del Bluetooth")
#Objetos de bluetooth
ble = bluetooth.BLE()
uart = BLEUART(ble, Nombre_Bluetooth)

def configuracion_Alarma(ultimatecla):
    global Tiempo_Alerta_glo  # Declara variables globales para manipular su estado
    global Estado_glo

    # Verifica si la última tecla presionada es un dígito
    if ultimatecla.isdigit():
        # Si es un dígito, lo añade al tiempo de alerta existente
        Tiempo_Alerta_glo = str(Tiempo_Alerta_glo) + str(ultimatecla)
        Pantalla.mostrar_mensaje()  # Llama a mostrar un mensaje genérico (posiblemente instrucciones)
        Pantalla.mostrar_mensaje_dig(Tiempo_Alerta_glo)  # Muestra el tiempo de alerta actualizado en la pantalla

    else:
        # Verifica si la última tecla es la letra 'A', que podría usarse para finalizar la entrada
        if ultimatecla == "A":
            # Asegura que el tiempo de alerta no está vacío antes de proceder
            if Tiempo_Alerta_glo != "":
                # Convierte el tiempo de alerta de minutos a milisegundos
                tiempoAlerta = int(Tiempo_Alerta_glo) * 60000
                # Configura un temporizador que llama a `activar_alarma` cuando expira
                temporizador.init(mode=Timer.ONE_SHOT, period=tiempoAlerta, callback=Alarma.encender_zumbador)
                Estado_glo = 0  # Actualiza el estado global, posiblemente para indicar que la alarma está configurada
                Pantalla.mostrar_mensaje_info("Alerta configurada")# Informa al usuario que la alarma está configurada
            else:
                Pantalla.mostrar_mensaje_info("No config alamar")# Informa al usuario que no configuro alarma.
                Estado_glo = 0

        else:
            # Maneja la situación donde se presiona una tecla no válida
            if ultimatecla != "":
                Pantalla.mostrar_mensaje_info("Valor no valido")  # Informa al usuario sobre la entrada inválida
                Estado_glo = 0

def MonstrarTemp_Frec(timer):
    global Estado_glo
    print('Estado de la configuracion', str(Estado_glo))
    if Estado_glo == 0:
        temp=str(Lectures.get_temp())
        BMP=str(Lectures.get_max30102_values())
        Pantalla.mostrar_frecuencia_temperatura(BMP,temp)

#Metodo que identifica los comando por bluetooth
def on_rx():
    # Lee los datos recibidos a través de UART y los decodifica a texto.
    rx_recibe = uart.read().decode().strip()
    
    # Envía una confirmación de lo que ha recibido de vuelta al emisor.
    uart.write("Esp-32 dice: " + str(rx_recibe) + "\n")
    
    # Imprime en la consola local lo que se ha recibido.
    print(rx_recibe)
    
    # Verifica si el comando recibido es para subir el espaldar de la camilla o silla.
    if rx_recibe == "!B516":
        # Llama a la función para ajustar el espaldar subiéndolo.
        Servos.configuracion_espaldar(PosicionServo)
        # Ejemplo de acción adicional, como encender un LED.
        print("enciende el led")
    
    # Verifica si el comando recibido es para bajar el espaldar.
    if rx_recibe == "!B615":
        # Llama a la función para ajustar el espaldar bajándolo.
        Servos.configuracion_espaldar((PosicionServo * -1))
    
    # Verifica si el comando recibido es para bajar el soporte de piernas.
    if rx_recibe == "!B714":
        # Llama a la función para ajustar el soporte de piernas bajándolo.
        Servos.configuracion_piernas((PosicionServo * -1))
    
    # Verifica si el comando recibido es para subir el soporte de piernas.
    if rx_recibe == "!B813":
        # Llama a la función para ajustar el soporte de piernas subiéndolo.
        Servos.configuracion_piernas(PosicionServo)
    
    # Verifica si el comando recibido es para subir la altura total de la camilla.
    if rx_recibe == "!B11:":
        # Llama a la función para ajustar la altura subiéndola.
        Servos.configuracion_Altura(PosicionServo)
    
    # Verifica si el comando recibido es para bajar la altura total de la camilla.
    if rx_recibe == "!B318":
        # Llama a la función para ajustar la altura bajándola.
        Servos.configuracion_Altura((PosicionServo * -1))


# Configura una interrupción en la UART para manejar automáticamente la recepción de datos utilizando la función on_rx como manejador de la interrupción.
uart.irq(handler = on_rx)
#Inicio la funcion que establece las teclas arriba.
Teclado.inicio()
#Inicia el timer que muestra la frecuencia y la temperatura
temporizador_Frec_Temp.init(mode=Timer.PERIODIC, period=Tiempo_Temperatura, callback=MonstrarTemp_Frec)
#
Pantalla.mostrar_mensaje_info("Cargando...")
while True:
    ultimatecla = Teclado.ultima_tecla_presionada()
    if ultimatecla == "C":
        Alarma.apagar_zumbador()
    if Estado_glo == 1:
        configuracion_Alarma(ultimatecla)
    if Estado_glo == 0 and ultimatecla == "D":
        Estado_glo = 1
        Pantalla.mostrar_mensaje()

    
    