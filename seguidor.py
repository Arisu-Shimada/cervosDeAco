import wiringpi as pi
from wiringpi import GPIO as io
import time
import testeOled as ini
import testeMotor as mt
import processaImagem as prImg
import cv2
import numpy as np


#Setup dos GPIOs:
pi.wiringPiSetup()

#GPIOs Utilizados
pi.pinMode(23, io.OUTPUT)
pi.pinMode(24, io.OUTPUT)
pi.pinMode(25, io.OUTPUT)
pi.pinMode(26, io.OUTPUT)
pi.pinMode(5, io.OUTPUT)

#Programa principal

camIndex = 11 #'v4l2:///dev/videoCam'

camera = cv2.VideoCapture(camIndex, cv2.CAP_V4L2)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

kp = 0
ki = 0
kd = 0
DirecaoAnterior = 0
botao = False

def pid(kp, ki, kd):
    i = i + Direcao
    d = Direcao - DirecaoAnterior
    correcao = (kp * Direcao) + (ki * i) + (kd * d)
    return correcao

while True:
    pi.digitalWrite(5, io.HIGH)
    ini.iniciarCod()
    try:    
        for i in range(0, 20):
            (grabbed, Frame) = camera.read()
            time.sleep(0.01)
            if not grabbed:
                print("Câmera desconectada! Tentando reconectar...")
                camera.release()
                time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
                camera = cv2.VideoCapture(camIndex, cv2.CAP_V4L2)
                camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
                continue 
        while True:
            (grabbed, Frame) = camera.read()
            # Se a câmera desconectar ou o frame falhar
            if not grabbed:
                print("Câmera desconectada! Tentando reconectar...")
                camera.release()    
                time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
                camera = cv2.VideoCapture(camIndex, cv2.CAP_V4L2)
                camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
                continue            
            if (grabbed):        
                Direcao, QtdeLinhas = prImg.TrataImagem(Frame)
                correcao = pid(kp, ki, kd)
                if(botao == True):
                    pi.digitalWrite(5, io.LOW)
                    mt.motor(0, 0)
                    break
                if (QtdeLinhas == 0 and botao == False):
                    print("Nenhuma linha encontrada. O robo ira parar.")                    
                    mt.motor(0, 0)
                    continue
                if (Direcao > 115 and botao == False):
                    while(Direcao > 95):
                        (grabbed, Frame) = camera.read()
                        Direcao, QtdeLinhas = prImg.TrataImagem(Frame)
                        print("Distancia da linha de referencia: " + str(abs(Direcao)) + " pixels a direita")
                        mt.motor(1, -1)
                        if(ini.lerBotao() == True):                    
                            botao = True
                            break
                        time.sleep(0.1)
                    time.sleep(0.5)
                    mt.motor(1, 1)
                if (Direcao < 70 and botao == False):
                    while(Direcao < 85):
                        (grabbed, Frame) = camera.read()
                        Direcao, QtdeLinhas = prImg.TrataImagem(Frame)
                        print("Distancia da linha de referencia: " + str(abs(Direcao)) + " pixels a esquerda")
                        mt.motor(-1, 1)
                        if(ini.lerBotao() == True):                    
                            botao = True
                            break
                        time.sleep(0.1)
                    time.sleep(0.5)
                    mt.motor(1, 1)
                if (Direcao < 95 and Direcao > 85 and botao == False):
                    print("Exatamente na linha de referencia!")
                    mt.motor(1, 1)
                if(ini.lerBotao() == True):                    
                    botao = True
                    break
                DirecaoAnterior = Direcao       
            time.sleep(0.01)
            botao = False
    except (KeyboardInterrupt):
        pi.digitalWrite(5, io.LOW)
        print("programa encerrado") 
        mt.motor(0, 0)
        camera.release()
        cv2.destroyAllWindows()
        exit(1)
    botao = False
    time.sleep(0.01)
