'''Forçar Resolução no OpenCV
Algumas webcams USB desconectam quando o OpenCV 
tenta capturar imagens em uma resolução/taxa de quadros 
não suportada nativamente. Forçar a resolução logo após 
instanciar a câmera pode estabilizar a conexão:'''

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#---------------------------------------------------------------------
'''Forçar a reconexão automática (Loop de segurança)
Se o cabo da câmera sofrer uma leve oscilação ou se for 
uma câmera IP e perder a conexão, o cap.read() retornará 
False e poderá travar o seu código. Adicione um bloco para 
tentar reabrir a porta de vídeo:'''

import cv2
import time

def get_video_capture(camera_id=0):
    return cv2.VideoCapture(camera_id)

cap = get_video_capture(0)

while True:
    ret, frame = cap.read()
    
    # Se a câmera desconectar ou o frame falhar
    if not ret:
        print("Câmera desconectada! Tentando reconectar...")
        cap.release()
        time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
        cap = get_video_capture(0)
        continue
    
    cv2.imshow("Video", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#---------------------------------------------------------------------
''' Liberar a câmera corretamente (release()
Se a sua câmera congela, fica com a luz acesa no notebook 
ou dá erro na segunda vez que você roda o código, 
é porque o programa não liberou o recurso corretamente. 
Certifique-se de que o método .release() está no final do código ou 
dentro da condição de saída:'''

cap.release()
cv2.destroyAllWindows()