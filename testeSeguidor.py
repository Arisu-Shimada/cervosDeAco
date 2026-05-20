import cv2
import numpy as np

# Load image and convert to grayscale
image = cv2.imread('curva.png')
height = np.size(image, 0)
width = np.size(image, 1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)
#cv2.imshow('Grayscale Image', gray)
#cv2.waitKey(0)

# Threshold to get a binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
thresh = cv2.dilate(thresh,None,iterations=2)
thresh = cv2.bitwise_not(thresh)

#cv2.imshow('Thresholded Image', thresh)
#cv2.waitKey(0)

# Find contours using CHAIN_APPROX_SIMPLE
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    # 3. Aproximação Poligonal
    # peri: perímetro do contorno
    peri = cv2.arcLength(cnt, True)
    # Aproxima o contorno com 2% a 4% de precisão do perímetro
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    if len(approx) >= 4: # Verifica se é uma forma geométrica
        print(f"Vértices encontrados: {len(approx)}")
        print(approx) # Coordenadas (x, y) dos vértices
        
        # Desenhar os vértices na imagem
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)

        pd1 = approx[0][0][0] + ((approx[len(approx)-1][0][0] - approx[0][0][0]) / 2)
        pd2 = approx[len(approx)-1][0][1]
        cv2.circle(image, (int(pd1), int(pd2)), 10, (255, 0, 0), -1) # Desenha um círculo azul no ponto de destino

        cv2.circle(image, (width//2, height), 10, (0, 255, 0), -1) # Desenha um círculo verde no ponto do robo

angulo = np.arctan2(pd2 - height, pd1 - (width//2)) * -180 / np.pi
print(f"Ângulo de direção: {int(angulo)+1} graus")
# Draw contours
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()