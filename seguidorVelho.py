import wiringpi as pi
from wiringpi import GPIO as io
import time

pi.wiringPiSetup()

pi.pinMode(5,io.INPUT)
pi.pinMode(6, io.INPUT)
pi.pinMode(23, io.OUTPUT)
pi.pinMode(24, io.OUTPUT)
pi.pinMode(25, io.OUTPUT)
pi.pinMode(26, io.OUTPUT)

try:
	while True:
		sensor1 = pi.digitalRead(5)
		sensor2 = pi.digitalRead(6)
		print(sensor1, sensor2)

		if(sensor1 == 0 and sensor2 == 0):
			print("Frente")
			pi.digitalWrite(23, io.LOW)
			pi.digitalWrite(24, io.HIGH)
			pi.digitalWrite(25, io.HIGH)
			pi.digitalWrite(26, io.LOW)
		if(sensor1 == 0 and sensor2 == 1):
			print("Direita")
			pi.digitalWrite(23, io.LOW)
			pi.digitalWrite(24, io.HIGH)
			pi.digitalWrite(25, io.LOW)
			pi.digitalWrite(26, io.HIGH)
		if(sensor1 == 1 and sensor2 == 0):
			print("Esquerda")
			pi.digitalWrite(23, io.HIGH)
			pi.digitalWrite(24, io.LOW)
			pi.digitalWrite(25, io.HIGH)
			pi.digitalWrite(26, io.LOW)
		elif(sensor1 == 1 and sensor2 == 1):
			print("Sem linha")
			pi.digitalWrite(23, io.LOW)
			pi.digitalWrite(24, io.LOW)
			pi.digitalWrite(25, io.LOW)
			pi.digitalWrite(26, io.LOW)
		time.sleep(0.01)

except KeyboardInterrupt:
	print("programa encerrado")
	pi.digitalWrite(23, io.LOW)
	pi.digitalWrite(24, io.LOW)
	pi.digitalWrite(25, io.LOW)
	pi.digitalWrite(26, io.LOW)
