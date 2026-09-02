from ev3dev2.motor import LargeMotor, SpeedPercent, MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from ev3dev2 import list_devices
from ev3dev2.sensor.lego import InfraredSensor
#from ev3dev2.sensor import INPUT_1
#from ev3dev2.sensor import INPUT_2
from ev3dev.ev3 import *
from ev3dev2.led import Leds
from time import sleep, time
import serial

porta = '/dev/ttyUSB0'
baud = 115200

ser = serial.Serial(porta, baudrate=baud, timeout=1)

# Define os motores
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

# Define os sensores de cor
sensor_esq = ColorSensor(INPUT_1)
sensor_dir = ColorSensor(INPUT_2)
sensor_dist = InfraredSensor(INPUT_3)

sensor_esq.mode = 'COL-COLOR'
sensor_dir.mode = 'COL-COLOR'

# Define a velocidade do robo
velocidade = 30  # Ajuste conforme necessario

def resgate():
