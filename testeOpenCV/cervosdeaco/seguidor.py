from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from ev3dev2 import list_devices
from ev3dev2.sensor.lego import InfraredSensor
#from ev3dev2.sensor import INPUT_1
#from ev3dev2.sensor import INPUT_2
from ev3dev.ev3 import *
from time import sleep

# Define os motores
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Define os sensores de cor
sensor_esq = ColorSensor(INPUT_1)
sensor_dir = ColorSensor(INPUT_2)
sensor_dist = InfraredSensor(INPUT_3)

sensor_esq.mode = 'COL-COLOR'
sensor_dir.mode = 'COL-COLOR'

veri = False

# Define a velocidade do robô
velocidade = 30  # Ajuste conforme necessário

def doisPreto_esq():
    tank_drive.on_for_rotations(50, -50, 0.1)
    tank_drive.on_for_rotations(50, 50, 0.5)
    while(not Button().enter):
        print("dois preto em uma moto")
        tank_drive.on(-50, 50)
        # Lê os valores dos sensores
        valor_esq = sensor_esq.value()
        valor_dir = sensor_dir.value()
        if(sensor_dir != 6):
            tank_drive.on(velocidade, velocidade)
            break
        """if(sensor_esq == 3 or sensor_dir == 3):
            tank_drive.on(velocidade, velocidade)
            break"""
def doisPreto_dir():
    tank_drive.on_for_rotations(-50, 50, 0.1)
    tank_drive.on_for_rotations(50, 50, 0.5)
    while(not Button().enter):
        print("dois preto em uma moto")
        tank_drive.on(50, -50)
        # Lê os valores dos sensores
        valor_esq = sensor_esq.value()
        valor_dir = sensor_dir.value()
        if(sensor_esq != 6):
            tank_drive.on(velocidade, velocidade)
            break
        """if(sensor_esq == 3 or sensor_dir == 3):
            tank_drive.on(velocidade, velocidade)
            break"""

def seguir_linha():
    """Funcao principal para seguir a linha."""
    
    while not Button().enter:
        # Lê os valores dos sensores
        valor_esq = sensor_esq.value()
        valor_dir = sensor_dir.value()
        valor_dist = sensor_dist.value()

        print(sensor_dir.value())
        print(sensor_esq.value())

        if (valor_dist <= 5):
            desviarBloco()
        # Verifica a posição na linha
        if (valor_esq != 1 and valor_esq != 3 and valor_dir != 1 and valor_dir != 3):
            # Ambos sensores sobre branco (fora da linha), segue em frente
            tank_drive.on(velocidade, velocidade)
        elif (valor_esq == 1):
            # Sensor esquerdo sobre a linha (preto), curva para a esquerda
            print("fora")
            while(not Button().enter):
                print("dentro")
                tank_drive.on(-55, 55)
                # Lê os valores dos sensores
                valor_esq = sensor_esq.value()
                valor_dir = sensor_dir.value()
                
                if(sensor_dir != 6 and sensor_esq != 6):
                    doisPreto_esq()
                    break
                if(valor_esq == 6):
                    tank_drive.on(velocidade, velocidade)
                    print("saiu")
                    break
                if(sensor_esq == 3 or sensor_dir == 3):
                    break
                print(valor_esq)

        elif (valor_dir == 1):
            print("Fora")
            # Sensor direito sobre a linha (preto), curva para a direita
            while(not Button().enter):
                print("dentro")
                tank_drive.on(55, -55)

                # Lê os valores dos sensores
                valor_esq = sensor_esq.value()
                valor_dir = sensor_dir.value()
                
                if(sensor_dir == 1 and sensor_esq == 1):
                    doisPreto_dir()
                    break
                if(valor_dir == 6):
                    tank_drive.on(velocidade, velocidade)
                    print("saiu")
                    break
                if(sensor_esq == 3 or sensor_dir == 3):
                    break
                print(valor_dir)
        
        #sleep(0.01)  # Pequeno delay para evitar travamentos e leitura rápida dos sensores
    tank_drive.off()
def desviarBloco():
    tank_drive.on_for_rotations(-50, -50, 0.1)
    tank_drive.on_for_rotations(-50, 50, 1.3)
    tank_drive.on(70, 25)
    while (not Button().enter):
        if (veri == True):
            break
        if (sensor_esq == 1):
            tank_drive.on_for_rotations(velocidade, velocidade, 0.5)
            while (not Button().enter):
                if (sensor_esq == 1):
                    break
                tank_drive.on(-50, 50)
            veri = True
    veri = False



# Programa Principal
if __name__ == "__main__":
    # Inicia o loop para seguir a linha
    seguir_linha()