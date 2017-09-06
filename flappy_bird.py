import ssd1306
from framebuf import FrameBuffer as FB
from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(13, Pin.IN)
bird = '07e018f021f871ecf9ecfcfcbe7e4c81717e4082307c0f80'

def random(a,b):                                                            
    result = uos.urandom(1)[0]                                              
    result /= 256                                                           
    result *= b-a                                                           
    result += a                                                             
    return int(result)

def to_bytearray(s):
    return bytearray([int('0x'+s[i:i+2]) for i in range(0,len(s),2)])

def cls():
    oled.fill(0)
    oled.show()

sprite = FB(to_bytearray(bird),16,12,3)

up = FB(bytearray(64),16,32,3)
up.rect(2,0,12,27,1)
up.rect(0,26,16,6,1)

down = FB(bytearray(64),16,32,3)                         
down.rect(2,5,12,27,1)
down.rect(0,0,16,6,1)

y = 24
vel = 0
pressed = False
x_tower1 = 128
x_tower2 = 196
y_tower1 = random(20,42)
y_tower2 = random(20,42)

def move():
    global vel, y
    vel += .5
    y += vel
    if y > 47:
        y = 47
        vel = 0

def scroll():
    global x_tower1, x_tower2, y_tower1, y_tower2
    x_tower1 -= 3
    x_tower2 -= 3
    if x_tower1 < -15:
        x_tower1 = 128
        y_tower1 = random(20,42)
    if x_tower2 < -15:
        x_tower2 = 128
        y_tower2 = random(20,42)

def flap():
    global vel, pressed
    vel = -4
    pressed = True    

while True:
    if button.value() == 1 and not pressed:
        flap()
    if button.value() == 0 and pressed:
        pressed = False
    move()
    scroll()
    oled.fill(0)
    oled.framebuf.blit(sprite, 0, round(y))
    oled.framebuf.blit(up,x_tower1,y_tower1-46)
    oled.framebuf.blit(down,x_tower1,y_tower1+18)
    oled.framebuf.blit(up,x_tower2,y_tower2-46)
    oled.framebuf.blit(down,x_tower2,y_tower2+18)
    oled.show()