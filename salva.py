import cv2
import numpy as np

# Iniciar captura de vídeo
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret: break

    # 1. Converter BGR para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. Definir o intervalo da cor vermelha em HSV
    # Vermelho tem dois intervalos no HSV (0-10 e 170-180)
    lower_red = np.array([45, 80, 40])
    upper_red = np.array([75, 255, 255])
    
    # 3. Criar a máscara para detectar o vermelho
    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    qtdContour = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Ajuste o valor conforme necessário
            frame = cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            qtdContour = len(contours)

    # 4. Aplicar a máscara na imagem original
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostrar resultados
    cv2.imshow('Original', frame)
    cv2.imshow('Mascara', mask)
    cv2.imshow('Resultado', result)
    print("qtd contornos: ", qtdContour)

    # Sair com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
