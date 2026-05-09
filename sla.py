import time
import cv2
import numpy as np

LimiarBinarizacao = 55       #este valor eh empirico. Ajuste-o conforme sua necessidade 
AreaContornoLimiteMin = 100000  #este valor eh empirico. Ajuste-o conforme sua necessidade

#GPIOs utilizados:


#Funcao: trata imagem e retorna se o robo seguidor de linha deve ir para a esqueda ou direita
#Parametros: frame capturado da webcam e primeiro frame capturado
#Retorno: < 0: robo deve ir para a direita
#         > 0: robo deve ir para a esquerda
#         0:   nada deve ser feito
def TrataImagem(img):
    #obtencao das dimensoes da imagem
    height = np.size(img,0)
    width= np.size(img,1)
    QtdeContornos = 0
    DirecaoASerTomada = 0

    #tratamento da imagem
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    FrameBinarizado = cv2.threshold(gray,LimiarBinarizacao,255,cv2.THRESH_BINARY)[1]
    FrameBinarizado = cv2.dilate(FrameBinarizado,None,iterations=2)
    FrameBinarizado = cv2.bitwise_not(FrameBinarizado)

    #descomente as linhas abaixo se quiser ver o frame apos binarizacao, dilatacao e inversao de cores
    cv2.imshow('F.B.',FrameBinarizado)
    cv2.waitKey(10)

    cnts, _ = cv2.findContours(FrameBinarizado.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,cnts,-1,(255,0,255),3)
    for c in cnts:

        QtdeContornos = QtdeContornos + 1

        # 3. Aproximação Poligonal
        # peri: perímetro do contorno
        peri = cv2.arcLength(c, True)
        # Aproxima o contorno com 2% a 4% de precisão do perímetro
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) >= 4: # Verifica se é uma forma geométrica
            #print(f"Vértices encontrados: {len(approx)}")
            #print(approx) # Coordenadas (x, y) dos vértices

            # Desenhar os vértices na imagem
            cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)

            pd1 = approx[0][0][0] + ((approx[len(approx)-1][0][0] - approx[0][0][0]) / 2)
            pd2 = approx[len(approx)-1][0][1]
            cv2.circle(img, (int(pd1), int(pd2)), 10, (255, 0, 0), -1) # Desenha um círculo azul no ponto de destino

            cv2.circle(img, (width//2, height), 10, (0, 255, 0), -1) # Desenha um círculo verde no ponto do robo

            angulo = np.arctan2(pd2 - height, pd1 - (width//2)) * -180 / np.pi
            print(f"Ângulo de direção: {int(angulo)+1} graus") 
    
            DirecaoASerTomada = int(angulo)+1
    #output da imagem
    #linha em azul: linha central / referencia
    #linha em verde: linha que mostra distancia entre linha e a referencia
    '''
    cv2.line(img,(int(width/2),0),(int(width/2),height),(255,0,0),2)
    
    if (QtdeContornos > 0):
        cv2.line(img,PontoCentralContorno,(int(width/2),CoordenadaYCentroContorno),(0,255,0),1)

    '''
    
    cv2.imshow('Analise de rota',img)
    cv2.waitKey(10)
    return DirecaoASerTomada, QtdeContornos


#Programa principal

#Setup dos GPIOs:

camera = cv2.VideoCapture(1)
camera.set(3,320)
camera.set(4,240)

while True:
    try:    
        for i in range(0, 20):
            (grabbed, Frame) = camera.read()
        while True:
            (grabbed, Frame) = camera.read()
            if (grabbed):
                Direcao, QtdeLinhas = TrataImagem(Frame[160:320, 0:240])
                if (QtdeLinhas == 0):
                    print("Nenhuma linha encontrada. O robo ira parar.")
                    continue
                if (Direcao > 90):
                    print("Distancia da linha de referencia: " + str(abs(Direcao)) + " pixels a direita")                    
                if (Direcao < 90):
                    print("Distancia da linha de referencia: " + str(abs(Direcao)) + " pixels a esquerda")                
                if (Direcao == 90):
                    print("Exatamente na linha de referencia!")                                    
                time.sleep(0.01)
    except (KeyboardInterrupt):
        print("programa encerrado")         
        exit(1)   