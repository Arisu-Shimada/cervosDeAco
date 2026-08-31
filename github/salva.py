import cv2
import numpy as np
import time

LimiarBinarizacao = 55       #este valor eh empirico. Ajuste-o conforme sua necessidade 
AreaContornoLimiteMin = 100000  #este valor eh empirico. Ajuste-o conforme sua necessidade
global pd1
global pd2

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

    def verde (img):
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

        # Ignorar contornos muito pequenos
        if cv2.contourArea(c) < 100: continue

        # 3. Obter o retângulo mínimo rotacionado (centro, tamanho, angulo)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect) # Obtém os 4 vértices
        box = np.intc(box) # Converte para inteiros

        # 4. Desenhar o retângulo (opcional)
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

        # 5. Identificar os lados
        # box contém os vértices ordenados
        p1, p2, p3, p4 = box[0], box[1], box[2], box[3]

        # Lados são p1-p2, p2-p3, p3-p4, p4-p1
        def dist(pa, pb):
            return np.linalg.norm(pa - pb)

        lados = [
            (p1, p2, (p1+p2)/2), # lado 1 e seu ponto médio
            (p2, p3, (p2+p3)/2),
            (p3, p4, (p3+p4)/2),
            (p4, p1, (p4+p1)/2)
        ]

        # Ordenar lados pelo comprimento
        lados.sort(key=lambda x: dist(x[0], x[1]))

        # 6. Os dois menores lados (menores comprimentos)
        menor_lado1 = lados[0][2] # Ponto médio 1
        menor_lado2 = lados[1][2] # Ponto médio 2

        # Desenhar os pontos centrais
        cv2.circle(img, ((width//2), height), 5, (255, 0, 0), -1)
        cv2.circle(img, tuple(menor_lado2.astype(int)), 5, (0, 0, 255), -1)

        delta_x = menor_lado2[0] - (width//2)
        delta_y = menor_lado2[1] - height

        angulo = np.arctan2(delta_y, delta_x) * -180 / np.pi
        print(f"Ângulo de direção: {int(angulo)+1} graus") 

        DirecaoASerTomada = int(angulo)+1

        DirecaoASerTomada = 0

        QtdeContornos = QtdeContornos + 1

        if (verde(img) == 0):
            DirecaoASerTomada = 180
        if (verde(img) == 1):
            DirecaoASerTomada = 0

    return DirecaoASerTomada, QtdeContornos


#Programa principal

#Setup dos GPIOs:
camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

kp = 0
ki = 0
kd = 0
i = 0
DirecaoAnterior = 0

while True:
    try:    
        for i in range(0, 20):
            (grabbed, Frame) = camera.read()
        while True:
            (grabbed, Frame) = camera.read()
            if (grabbed):
                Direcao, QtdeLinhas = TrataImagem(Frame[160:320, 0:240])
                i = i + Direcao
                d = Direcao - DirecaoAnterior
                correcao = (kp * Direcao) + (ki * i) + (kd * d)
                if (QtdeLinhas == 0):
                    print("Nenhuma linha encontrada. O robo ira parar.")
                if (Direcao > 90):
                    print("Distancia da linha de referencia: " + str(abs(Direcao)) + " pixels a direita")                    
                if (Direcao < 90):
                    print("Distancia da linha de referencia: " + str(abs(Direcao)) + " pixels a esquerda")                
                if (Direcao == 90):
                    print("Exatamente na linha de referencia!")    
                DirecaoAnterior = Direcao         
                cv2.imshow('Analise de rota',Frame)
                cv2.waitKey(10)
            time.sleep(0.01)
    except (KeyboardInterrupt):
        print("programa encerrado")  
        cv2.release(camera)       
        cv2.destroyAllWindows()
        exit(1)  
    time.sleep(0.01)                       