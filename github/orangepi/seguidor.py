import wiringpi as pi
from wiringpi import GPIO as io
import time
import testeOled as ini
import testeMotor as mt
import cv2

pi.wiringPiSetup()

pi.pinMode(5,io.INPUT)
pi.pinMode(6, io.INPUT)
pi.pinMode(23, io.OUTPUT)
pi.pinMode(24, io.OUTPUT)
pi.pinMode(25, io.OUTPUT)
pi.pinMode(26, io.OUTPUT)

vel = 0

def desviar(sensor1,sensor2,sensorObs):
	verificacao = False
	mt.motor(-1,-1)
	time.sleep(0.1)
	mt.motor(1,-1)
	time.sleep(0.7)
	mt.motor(0,1)
	while True:
		print(sensor1, sensor2, sensorObs)
		sensor1 = pi.digitalRead(5)
		sensor2 = pi.digitalRead(6)
		sensorObs = pi.digitalRead(7)
		if(verificacao == True):
			break
		if(sensor2 == 1):
			mt.motor(1,1)
			time.sleep(0.3)
			while True:
				print(sensor1, sensor2, sensorObs)
				sensor1 = pi.digitalRead(5)
				sensor2 = pi.digitalRead(6)
				sensorObs = pi.digitalRead(7)
				if(sensor2 == 1):
					break
				mt.motor(1,-1)
				time.sleep(0.01)
			verificacao = True
		time.sleep(0.01)
	verificacao = False
try:
	while True:
		ini.iniciarCod()
		while True:
			sensor1 = pi.digitalRead(5)
			sensor2 = pi.digitalRead(6)
			sensorObs = pi.digitalRead(7)
			print(sensor1, sensor2, sensorObs)
			if(sensor1 == 0 and sensor2 == 0):
				print("Frente")
				mt.motor(1,1,vel)
			if(sensor1 == 0 and sensor2 == 1):
				print("Direita")
				mt.motor(0,0,vel)
				while True:
					sensor1 = pi.digitalRead(5)
					sensor2 = pi.digitalRead(6)
					mt.motor(1,-1,vel)
					if(sensor2 == 0):
						print("stopped")
						break
					if(sensor1 == 1 and sensor2 == 1):
						mt.motor(-1,1,vel)
						time.sleep(0.2)
						mt.motor(1,1,vel)
						time.sleep(0.5)
						while True:
							sensor1 = pi.digitalRead(5)
							sensor2 = pi.digitalRead(6)
							mt.motor(1,-1,vel)
							if(sensor1 == 1):
								break
						mt.motor(-1,1,vel)
						time.sleep(0.2)
						break
			if(sensor1 == 1 and sensor2 == 0):
				print("Esquerda")
				mt.motor(0,0,vel)
				while True:
					sensor1 = pi.digitalRead(5)
					sensor2 = pi.digitalRead(6)
					mt.motor(-1,1,vel)
					if(sensor1 == 0):
						print("stopped")
						break
					if(sensor1 == 1 and sensor2 == 1):
						mt.motor(1,-1,vel)
						time.sleep(0.2)
						mt.motor(1,1,vel)
						time.sleep(0.5)
						while True:
							sensor1 = pi.digitalRead(5)
							sensor2 = pi.digitalRead(6)
							mt.motor(-1,1,vel)
							if(sensor2 == 1):
								break
						mt.motor(1,-1,vel)
						time.sleep(0.2)
						break
			elif(sensor1 == 1 and sensor2 == 1):
				print("Sem linha")
				mt.motor(1,1,vel)
			#if(sensorObs == 1):
			#	desviar(sensor1, sensor2, sensorObs)
			ini.lerBotao()
			if(ini.lerBotao() == True):
				mt.motor(0,0,vel)
				time.sleep(1)
				break
			time.sleep(0.01)
except KeyboardInterrupt:
	print("programa encerrado")
	mt.motor(0,0,vel)