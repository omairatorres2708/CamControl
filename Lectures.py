from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from machine import sleep, SoftI2C, Pin, Timer 
from utime import ticks_diff, ticks_us


#led = Pin(2, Pin.OUT)

MAX_HISTORY = 32 #Tamaño máximo del historial para almacenar lecturas.
history = [] # Lista para almacenar las lecturas de la señal.
beats_history = [] #Lista para almacenar los BPM calculados.
beat = False #Indica si se detectó un latido.
beats = 0 #promedio de beats
    
i2c = SoftI2C(sda=Pin(21),scl=Pin(22),freq=400000)
sensor = MAX30102(i2c=i2c)  # An I2C instance is required

# Scan I2C bus to ensure that the sensor is connected
if sensor.i2c_address not in i2c.scan():
    print("Sensor not found.")
    
elif not (sensor.check_part_id()):
    # Check that the targeted sensor is compatible
    print("I2C device ID not corresponding to MAX30102 or MAX30105.")
    
else:
    print("Sensor connected and recognized.")

# It's possible to set up the sensor at once with the setup_sensor() method.
# If no parameters are supplied, the default config is loaded:
# Led mode: 2 (RED + IR)
# ADC range: 16384
# Sample rate: 400 Hz
# Led power: maximum (50.0mA - Presence detection of ~12 inch)
# Averaged samples: 8
# pulse width: 411
print("Setting up sensor with default configuration.", '\n')
sensor.setup_sensor() #onfigura el sensor con parámetros predeterminados.

# It is also possible to tune the configuration parameters one by one.
# Set the sample rate to 400: 400 samples/s are collected by the sensor
sensor.set_sample_rate(400)
# Set the number of samples to be averaged per each reading
sensor.set_fifo_average(8) #Establece el promedio de muestras por lectura.
# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM) #Configura la amplitud de los LEDs.
sensor.set_led_mode(2) # Establece el modo LED a RED + IR.
sleep(1)

# The readTemperature() method allows to extract the die temperature in °C
def get_temp():
    print("Lectura de temperatura en C.")
    return(sensor.read_temperature())
    

t_start = ticks_us()  # Starting time of the acquisition   


def get_max30102_values():
    while True:
        global history
        global beats_history
        global beat
        global beats
        global t_start
        flag= False
        sensor.check()
        
        # Check if the storage contains available samples
        if sensor.available():
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()
            
            value = red_reading
            history.append(value)
            # Get the tail, up to MAX_HISTORY length
            history = history[-MAX_HISTORY:]
            minima = 0
            maxima = 0
            threshold_on = 0
            threshold_off = 0

            minima, maxima = min(history), max(history)

            threshold_on = (minima + maxima * 3) // 4   # 3/4
            threshold_off = (minima + maxima) // 2      # 1/2
            
            
            if value > 1000:
                if not beat and value > threshold_on:
                    beat = True 
                    t_us = ticks_diff(ticks_us(), t_start)
                    t_s = t_us/1000000
                    f = 1/t_s
                    bpm = f * 60
                    
                    if bpm < 500:
                        t_start = ticks_us()
                        beats_history.append(bpm)                    
                        beats_history = beats_history[-MAX_HISTORY:] 
                        beats = round(sum(beats_history)/len(beats_history) ,2)  
                                        
                if beat and value< threshold_off:
                    beat = False
                if (len(beats_history)>9):
                    print(beats_history)
                    beats_history=[] # si quiero tomar una nueva medida cada vez
                    return(beats)
                
            else:
                beats = 0.00
                beats_history=[]
                print('No dedo')
                return(beats)
                

            
           
                
                
        

            