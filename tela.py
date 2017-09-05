import ssd1306
import network
from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(13, Pin.IN)
sta_if = network.WLAN(network.STA_IF)
display_lines = ['' for i in range(8)]

def get_ip(interface):
    return interface.ifconfig()[0]

def show_lines():
    oled.fill(0)
    for line,text in enumerate(display_lines):
        oled.text(text, 0, line*8)
    oled.show()

def screen_off():
    oled.fill(0)
    oled.show()

def cls():
    global display_lines    
    display_lines = ['' for i in range(8)]
    show_lines()

def dprint(text):
    global display_lines
    display_lines.append(str(text))
    display_lines.pop(0)
    show_lines()
    
dprint('TELA LIGADA')


