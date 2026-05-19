import cv2
import numpy as np

# 1. Carregar imagem e pré-processar
image = cv2.imread('curva.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
thresh = cv2.dilate(thresh,None,iterations=2)
thresh = cv2.bitwise_not(thresh)

# 2. Encontrar contornos
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    # Ignorar contornos muito pequenos
    if cv2.contourArea(cnt) < 100: continue

    # 3. Obter o retângulo mínimo rotacionado (centro, tamanho, angulo)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect) # Obtém os 4 vértices
    box = np.intc(box) # Converte para inteiros

    # 4. Desenhar o retângulo (opcional)
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

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
    cv2.circle(image, tuple(menor_lado1.astype(int)), 5, (255, 0, 0), -1)
    cv2.circle(image, tuple(menor_lado2.astype(int)), 5, (255, 0, 0), -1)

cv2.imshow("Pontos Centrais Lados Menores", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
