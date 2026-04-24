import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import wiringpi as pi
from wiringpi import GPIO as io

pi.wiringPiSetup()

pi.pinMode(8, io.INPUT)
# Substitua o 'port' pelo número da sua interface I2C (0, 1, etc.)
# O address padrão é 0x3C
serial = i2c(port=2, address=0x3C)

# Cria uma instância do dispositivo SSD1306
device = ssd1306(serial)
def iniciarCod():    
    while True:
        button = pi.digitalRead(8)
        print(button)
        # Desenha na tela usando o objeto canvas
        with canvas(device) as draw:
            draw.text((30, 10), "Orange Pi", fill="white")
            draw.text((20, 25), "Iniciar o", fill="white")
            draw.text((40, 40), "Codigo", fill="white")
        time.sleep(0.01)
        if(button == 1):
            device.clear()
            with canvas(device) as draw:
                draw.text((30, 10), "Codigo iniciado", fill="white")
            break
def lerBotao():
    button = pi.digitalRead(8)
    print(button)
    if(button == 1):
        device.clear()
        with canvas(device) as draw:
            draw.text((30, 10), "Codigo Finalizado", fill="white")    
        return True