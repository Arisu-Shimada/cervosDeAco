import wiringpi as pi
from wiringpi import GPIO as io
import time
import testeOled as ini
import testeMotor as mt
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

LimiarBinarizacao = 55       #este valor eh empirico. Ajuste-o conforme sua necessidade 
AreaContornoLimiteMin = 100000  #este valor eh empirico. Ajuste-o conforme sua necessidade

global pd1
global pd2

def TrataImagem(img):
    if (img is None):
        print("Erro ao capturar a imagem da câmera!")
        return 0, 0
    #obtencao das dimensoes da imagem
    height = np.size(img,0)
    width= np.size(img,1)
    QtdeContornos = 0
    DirecaoASerTomada = 0

    def verde (img):
        if (img is None):
            print("Erro ao capturar a imagem da câmera!")
            return 0, 0
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if (x > width//2):
                    print("Obstaculo a direita detectado!")
                    return 0
                if (x < width//2):
                    print("Obstaculo a esquerda detectado!")
                    return 1
            time.sleep(0.01)
    #tratamento da imagem
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    FrameBinarizado = cv2.threshold(gray,LimiarBinarizacao,255,cv2.THRESH_BINARY)[1]
    FrameBinarizado = cv2.dilate(FrameBinarizado,None,iterations=2)
    FrameBinarizado = cv2.bitwise_not(FrameBinarizado)

    cnts, _ = cv2.findContours(FrameBinarizado.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,cnts,-1,(255,0,255),3)
    for c in cnts:

        QtdeContornos = QtdeContornos + 1
        peri = cv2.arcLength(c, True)

        # Aproxima o contorno com 2% a 4% de precisão do perímetro
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) >= 4: # Verifica se é uma forma geométrica
            #print(f"Vértices encontrados: {len(approx)}")
            #print(approx) # Coordenadas (x, y) dos vértices

            # Desenhar os vértices na imagem
            cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)

            pd1 = approx[0][0][0] + ((approx[len(approx)-1][0][0] - approx[0][0][0]) / 2)
            pd2 = approx[len(approx)-1][0][1]

            cv2.circle(img, (int(pd1), int(pd2)), 10, (255, 0, 0), -1) # Desenha um círculo azul no ponto de destino

            cv2.circle(img, (width//2, height), 10, (0, 0, 255), -1) # Desenha um círculo azul no ponto do robo

            angulo = np.arctan2(pd2 - height, pd1 - (width//2)) * -180 / np.pi
            print(f"Ângulo de direção: {int(angulo)+1} graus") 
    
            DirecaoASerTomada = int(angulo)+1

            if (verde(img) == 0):
                DirecaoASerTomada = 180
            if (verde(img) == 1):
                DirecaoASerTomada = 0
            cv2.imshow("Frame", img)
        time.sleep(0.01)
    return DirecaoASerTomada, QtdeContornos

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
                Direcao, QtdeLinhas = TrataImagem(Frame)
                i = i + Direcao
                d = Direcao - DirecaoAnterior
                correcao = (kp * Direcao) + (ki * i) + (kd * d)
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
                        Direcao, QtdeLinhas = TrataImagem(Frame)
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
                        Direcao, QtdeLinhas = TrataImagem(Frame)
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
