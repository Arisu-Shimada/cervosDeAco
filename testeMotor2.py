import CervosDeAco.testeMotor as mt
import CervosDeAco.testeOled as ini
from time import sleep

ini.iniciarCod()
sleep(0.5)
while True:
	print("Rodando...")
	mt.motor(1,1)
	if (ini.lerBotao() == True):
		mt.motor(0,0)
		break
	sleep(0.1)