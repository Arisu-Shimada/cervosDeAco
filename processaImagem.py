import time
import cv2
import numpy as np

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