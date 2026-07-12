import wiringpi as pi
from wiringpi import GPIO as io
import time

pi.wiringPiSetup()

pi.pinMode(23, io.OUTPUT)
pi.pinMode(24, io.OUTPUT)
pi.pinMode(25, io.OUTPUT)
pi.pinMode(26, io.OUTPUT)
'''pi.pinMode(2, io.PWM_OUTPUT)
pi.pinMode(21, io.PWM_OUTPUT)'''
	
'''def velocidadeMotor(velM1, velM2):
	pi.pwmWrite(2, velM1)
	pi.pwmWrite(21, velM2)'''

def motor(direcao1, direcao2):
	if(direcao1 == 1 and direcao2 == 1):
		pi.digitalWrite(23, io.LOW)
		pi.digitalWrite(24, io.HIGH)
		pi.digitalWrite(25, io.LOW)
		pi.digitalWrite(26, io.HIGH)
	if(direcao1 == -1 and direcao2 == -1):
		pi.digitalWrite(23, io.HIGH)
		pi.digitalWrite(24, io.LOW)
		pi.digitalWrite(25, io.HIGH)
		pi.digitalWrite(26, io.LOW)
	if(direcao1 == 1 and direcao2 == -1):
		pi.digitalWrite(23, io.HIGH) 
		pi.digitalWrite(24, io.LOW)
		pi.digitalWrite(25, io.LOW)
		pi.digitalWrite(26, io.HIGH)
	if(direcao1 == -1 and direcao2 == 1):
		pi.digitalWrite(23, io.LOW)
		pi.digitalWrite(24, io.HIGH)
		pi.digitalWrite(25, io.HIGH)
		pi.digitalWrite(26, io.LOW)
	if(direcao1 == 0 and direcao2 == 0):
		pi.digitalWrite(23, io.LOW)
		pi.digitalWrite(24, io.LOW)
		pi.digitalWrite(25, io.LOW)
		pi.digitalWrite(26, io.LOW)
