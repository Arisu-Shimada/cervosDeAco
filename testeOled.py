import time
import wiringpi as pi
from wiringpi import GPIO as io

pi.wiringPiSetup()

pi.pinMode(8, io.INPUT)
pi.pinMode(3, io.OUTPUT)
pi.pinMode(5, io.OUTPUT)

def iniciarCod():    
    while True:
        try:
            button = pi.digitalRead(8)
            print(button)
            if(button == 1):
                pi.digitalWrite(3, io.HIGH)
                break
            time.sleep(0.1)
        except (KeyboardInterrupt):
            pi.digitalWrite(5, io.LOW)
            print("programa encerrado") 
            exit(1)   
def lerBotao():
    button = pi.digitalRead(8)
    print(button)
    if(button == 1):
        pi.digitalWrite(3, io.LOW)
        return True