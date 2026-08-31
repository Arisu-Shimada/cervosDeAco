import cv2
import numpy as np

#Funcao: trata imagem e retorna se o robo seguidor de linha deve ir para a esqueda ou direita
#Parametros: frame capturado da webcam e primeiro frame capturado
#Retorno: < 0: robo deve ir para a direita
#         > 0: robo deve ir para a esquerda
#         0:   nada deve ser feito
def TrataImagem(img):
    y_inicial, y_final = 80, 200
    x_inicial, x_final = 100, 300

    # 3. Recortar a imagem
    img = img[y_inicial:y_final, x_inicial:x_final]
    #obtencao das dimensoes da imagem
    height = np.size(img,0)
    width= np.size(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # 3. Encontrar os contornos da linha
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma cópia da imagem para desenhar o trajeto
    trajeto_img = img.copy()

    # 4. Iterar pelos pontos (ex: varredura por linhas horizontais para encontrar o centro em cada altura)
    # Esse é um método muito comum para robôs seguidores de linha
    pontos_centro = []
    for y in range(0, height, 20):  # Analisa a imagem a cada 20 pixel de altura
        linha_pixels = thresh[y, :]
        indices_brancos = np.where(linha_pixels == 255)[0]

        if len(indices_brancos) > 0:
            centro_x = int(np.mean(indices_brancos))
            pontos_centro.append((centro_x, y))
    pontos = {}
    # 5. Desenhar o trajeto conectando os pontos encontrados
    if(len(pontos_centro) > 1):
        for i in range(len(pontos_centro) - 1):
            pt1 = pontos_centro[i]
            pt2 = pontos_centro[i + 1]
            print(f"Desenhando linha de {pt1} para {pt2}")  # Debug: mostra os pontos conectados
            pontos[i] = tuple([pt1, pt2])
            # Desenha uma linha vermelha (BGR: 0, 0, 255) com espessura 3
            cv2.line(trajeto_img, pt1, pt2, (0, 0, 255), 3)
    if(len(pontos) > 0):
        for pt in pontos:
            print(pontos[pt])
        print (f"proximo ponto: {pontos[0]}")

    cv2.imshow('Analise de rota',trajeto_img)
    cv2.waitKey(10)


#Programa principal

#Setup dos GPIOs:

camera = cv2.VideoCapture(1)
camera.set(3,320)
camera.set(4,240)

#faz algumas leituras de frames antes de consierar a analise
#motivo: algumas camera podem demorar mais para se "acosumar a luminosidade" quando ligam, capturando frames consecutivos com muita variacao de luminosidade. Para nao levar este efeito ao processamento de imagem, capturas sucessivas sao feitas fora do processamento da imagem, dando tempo para a camera "se acostumar" a luminosidade do ambiente
for i in range(0,20):
    (grabbed, Frame) = camera.read()

while True:
    try:
      (grabbed, Frame) = camera.read()
    
      if (grabbed):
          TrataImagem(Frame)
          """
          if (QtdeLinhas == 0):
             print("Nenhuma linha encontrada. O robo ira parar.")
             continue
        
          if (Direcao > 0):
              print("Distancia da linha de referencia: "+str(abs(Direcao))+" pixels a direita")
          if (Direcao < 0):
              print("Distancia da linha de referencia: "+str(abs(Direcao))+" pixels a esquerda")      
          if (Direcao == 0):
              print("Exatamente na linha de referencia!")
              """
    except (KeyboardInterrupt):
        print("encerrado")
        exit(1)   