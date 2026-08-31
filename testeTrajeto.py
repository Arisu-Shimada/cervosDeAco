import cv2
import numpy as np

# 1. Carregar a imagem
img = cv2.imread('curva3.png')
h, w, _ = img.shape

# 2. Converter para escala de cinza e binarizar (inverter para a linha preta ficar branca)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

# 3. Encontrar os contornos da linha
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Criar uma cópia da imagem para desenhar o trajeto
trajeto_img = img.copy()

# 4. Iterar pelos pontos (ex: varredura por linhas horizontais para encontrar o centro em cada altura)
# Esse é um método muito comum para robôs seguidores de linha
pontos_centro = []
for y in range(0, h, 20):  # Analisa a imagem a cada 20 pixel de altura
    linha_pixels = thresh[y, :]
    indices_brancos = np.where(linha_pixels == 255)[0]
    
    if len(indices_brancos) > 0:
        centro_x = int(np.mean(indices_brancos))
        pontos_centro.append((centro_x, y))
pontos = {}
# 5. Desenhar o trajeto conectando os pontos encontrados
for i in range(len(pontos_centro) - 1):
    pt1 = pontos_centro[i]
    pt2 = pontos_centro[i + 1]
    print(f"Desenhando linha de {pt1} para {pt2}")  # Debug: mostra os pontos conectados
    pontos[i] = tuple([pt1, pt2])
    # Desenha uma linha vermelha (BGR: 0, 0, 255) com espessura 3
    cv2.line(trajeto_img, pt1, pt2, (0, 0, 255), 3)
for pt in pontos:
    print(pontos[pt])
print (f"proximo ponto: {pontos[0]}")
# 6. Mostrar o resultado
cv2.imshow('Trajeto da Linha', trajeto_img)
cv2.waitKey(0)
cv2.destroyAllWindows()