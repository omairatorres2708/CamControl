# Importa la clase Pin para control de pines GPIO
from machine import Pin
# Importar las clases necesarias para el sleep
from time import sleep

Tecla_Arriba   = const(0) #Indica que la tecla esta abajo
Tecla_Abajo = const(1) # Indica que la tecla esta arriba

# Matrix que contiene las teclas
teclas = [
['1', '2', '3', 'A'], 
['4', '5', '6', 'B'], 
['7', '8', '9', 'C'], 
['*', '0', '#', 'D']
]
# Defininicón de Pines
filas = [2,4,5,18]
columnas = [12,14,27,26]
# Inicializa una lista vacía para almacenar los objetos Pin configurados como salidas.
pines_Filas = []

# Itera sobre cada número de pin especificado en la lista 'filas'.
for pin_nombre in filas:
    try:
        # Intenta crear un objeto Pin, configurándolo como salida.
        pin = Pin(pin_nombre, mode=Pin.OUT)
        
        # Si la configuración es exitosa, añade el objeto Pin a la lista pines_Filas.
        pines_Filas.append(pin)
        
        # Imprime un mensaje de confirmación indicando que el pin ha sido configurado correctamente.
        print("Pin configurado como salida:", pin_nombre)
    
    # Captura cualquier ValueError que pueda ocurrir si el pin no puede ser configurado como salida.
    except ValueError:
        # Imprime un mensaje de error si el pin no puede ser configurado como salida.
        print("No se pudo configurar el pin como salida:", pin_nombre, "- ¡El pin solo puede ser entrada!")

# Inicializa una lista vacía para almacenar los objetos Pin configurados como entradas.
pines_Columnas = []

# Itera sobre cada número de pin especificado en la lista 'columnas'.
for pin_nombre in columnas:
    try:
        # Intenta crear un objeto Pin, configurándolo como entrada con resistencia de pull-down.
        pin = Pin(pin_nombre, mode=Pin.IN, pull=Pin.PULL_DOWN)
        
        # Si la configuración es exitosa, añade el objeto Pin a la lista pines_Columnas.
        pines_Columnas.append(pin)
        
        # Imprime un mensaje de confirmación indicando que el pin ha sido configurado correctamente como entrada.
        print("Pin configurado como entrada con pull-down:", pin_nombre)
    
    # Captura cualquier ValueError que pueda ocurrir si el pin no puede ser configurado como entrada.
    except ValueError:
        # Imprime un mensaje de error si el pin no puede ser configurado como entrada.
        print("No se pudo configurar el pin como entrada:", pin_nombre, "- ¡El pin solo puede ser salida!")


def inicio():
    # Bucle que recorre todas las filas del teclado (4 filas en total)
    for fila in range(0,4):
        # Bucle que recorre todas las columnas en cada fila (4 columnas en total)
        for col in range(0,4):
            # Establece el valor del pin correspondiente a cada fila a bajo (0)
            pines_Filas[fila].value(0)



def escanear(fila, columna):
    # Configura el pin correspondiente a la fila dada a alto (1)
    pines_Filas[fila].value(1)
    
    # Inicializa la variable 'key' a None. Esta variable almacenará el estado de la tecla.
    key = None
    
    # Verifica si la tecla en la posición especificada está presionada (Tecla_Abajo)
    if pines_Columnas[columna].value() == Tecla_Abajo:
        key = Tecla_Abajo  # Si la tecla está presionada, asigna Tecla_Abajo a 'key'
    
    # Verifica si la tecla en la posición especificada no está presionada (Tecla_Arriba)
    if pines_Columnas[columna].value() == Tecla_Arriba:
        key = Tecla_Arriba  # Si la tecla no está presionada, asigna Tecla_Arriba a 'key'
    
    # Configura el pin correspondiente a la fila dada a bajo (0) para desactivar la fila después de la lectura
    pines_Filas[fila].value(0)
    
    # Retorna el estado de la tecla detectada (None, Tecla_Abajo o Tecla_Arriba)
    return key


def ultima_tecla_presionada():
    # Bucle que recorre todas las filas del teclado (4 filas en total)
    for fila in range(4):
        # Bucle que recorre todas las columnas en cada fila (4 columnas en total)
        for columna in range(4):
            # Llama al método 'escanear' para verificar si la tecla en la posición actual está presionada
            tecla = escanear(fila, columna)
            
            # Si la tecla está presionada (Tecla_Abajo), procede a identificar la tecla
            if tecla == Tecla_Abajo:
                # Imprime el carácter de la tecla presionada
                print("Tecla precionada: ", teclas[fila][columna])
                
                # Pausa la ejecución por 0.5 segundos para manejar el rebote de la tecla
                sleep(0.5)
                
                # Retorna el carácter correspondiente a la tecla presionada como una cadena de texto
                return str(teclas[fila][columna])
    
    # Si no se detecta ninguna tecla presionada, retorna una cadena vacía
    return ""
