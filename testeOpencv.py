import cv2
import time
import CervosDeAco.testeMotor as mt

# Inicializa a captura de vídeo (0 é a câmera padrão do notebook/computador)
cap = cv2.VideoCapture(1)

# Verifica se a câmera foi aberta com sucesso
if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

print("Streaming iniciado. Pressione Ctrl+C no terminal para parar.")

try:
    while True:
        # Lê o próximo frame da câmera
        ret, frame = cap.read()
        mt.motor(1, 1)  # Exemplo de comando para o motor (ajuste conforme necessário)
        
        # Verifica se o frame foi lido corretamente
        if not ret:
            print("Erro: Falha ao capturar o frame.")
            break
        
        # Exibe um print no terminal em vez de usar cv2.imshow
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Frame capturado | Resolução: {frame.shape[1]}x{frame.shape[0]}")
        
        # Pausa por 1 segundo para não poluir o terminal rapidamente 
        # (remova o time.sleep para testar na velocidade máxima)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStreaming interrompido pelo usuário.")
finally:
    # Libera a câmera e fecha todos os recursos
    cap.release()
    mt.motor(0, 0)  # Para os motores ao encerrar
    print("Câmera liberada. Programa encerrado.")
