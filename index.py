import serial
import time

port = 'COM11'
rate = 9600

def enviar ():
    while True:
        command = input("Digite 'H' para ligar ou 'L' para desligar: ").upper()
        if command in ('H', 'L'):
            ser.write(command.encode())
            print(command.encode())
        else:
            print("Comando inválido.")
        

try:
    ser = serial.Serial(port, rate)
    print(f"Conectado a porta: {port}")
    enviar()
except  serial.SerialException as e:
    print(f"Erro ao conectar: {e}")
    exit()

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Conexão fechada.")
