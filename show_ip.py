import ssd1306
import network
from machine import I2C, Pin


i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(14, Pin.IN)
state0 = 0
sta_if = network.WLAN(network.STA_IF)

def change_state(state):
    if state == 1:
        oled.text("OLA, MUNDO!", 20, 20)
        oled.text(sta_if.ifconfig()[0], 0, 36)
        oled.show()
    else:
        oled.fill(0)
        oled.show()

while True:
    state = button.value()
    if state != state0:
        change_state(state)
        state0 = state