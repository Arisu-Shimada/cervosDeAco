import wiringpi as pi
from wiringpi import GPIO as io
import time

pi.wiringPiSetup()

pi.pinMode(2, io.PWM_OUTPUT)
pi.pinMode(24, io.OUTPUT)
pi.pinMode(21, io.PWM_OUTPUT)
pi.pinMode(26, io.OUTPUT)
	
def motor(direcao1, direcao2, vel):
	if(direcao1 == 1 and direcao2 == 1):
		pi.digitalWrite(26, io.HIGH)
		pi.digitalWrite(24, io.HIGH)
		pi.pwmWrite(2, vel)
		pi.pwmWrite(21, vel)
	if(direcao1 == -1 and direcao2 == -1):
		pi.digitalWrite(26, io.LOW)
		pi.digitalWrite(24, io.LOW)
		pi.pwmWrite(2, vel)
		pi.pwmWrite(21, vel)
	if(direcao1 == 1 and direcao2 == -1):
		pi.digitalWrite(26, io.LOW)
		pi.digitalWrite(24, io.HIGH)
		pi.pwmWrite(2, vel)
		pi.pwmWrite(21, vel)
	if(direcao1 == -1 and direcao2 == 1):
		pi.digitalWrite(26, io.HIGH)
		pi.digitalWrite(24, io.LOW)
		pi.pwmWrite(2, vel)
		pi.pwmWrite(21, vel)
	if(direcao1 == 0 and direcao2 == 0):
		pi.digitalWrite(26, io.LOW)
		pi.digitalWrite(24, io.LOW)
		pi.pwmWrite(2, 0)
		pi.pwmWrite(21, 0)
