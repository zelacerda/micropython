import ssd1306
import network
import urequests
from machine import I2C, Pin
from dht import DHT11

UP = 0
DOWN = 1
state = UP # Initial button state 

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(14, Pin.IN)
sensor = DHT11(Pin(13))
sta_if = network.WLAN(network.STA_IF)

def get_ip(interface):
    return interface.ifconfig()[0]

def get_temperature(sensor):
    sensor.measure()
    return sensor.temperature()

def send_temperature(t):
    url = "http://things.ubidots.com/api/v1.6/devices/NodeMCU?token="
    token = "A1E-5ZY9vbCGtRiqVinrnhrQxgA4FDSBaA"
    url += token
    headers = {"Content-Type": "application/json"}
    data = '{"temperature": ' + str(t) + '}'
    urequests.post(url, data=data, headers=headers) 

def show_lines(strings):
    oled.fill(0)
    for line,text in enumerate(strings):
        oled.text(text, 0, line*10)
    oled.show()

def screen_off():
    oled.fill(0)
    oled.show()

def button_pressed():
    global state
    t = get_temperature(sensor)
    send_temperature(t)
    lines = ['IP:',
             get_ip(sta_if),
             '',
             'TEMPERATURA:',
             str(t)]
    show_lines(lines)
    state = DOWN

def button_released():
    global state
    screen_off()
    state = UP

while True:
    b = button.value()
    if b == DOWN and state == UP:
        button_pressed()
    elif b == UP and state == DOWN:
        button_released()