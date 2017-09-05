import ssd1306
import framebuf
from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(13, Pin.IN)
bird = [0x0000, 0x0000, 0x07e0, 0x18f0,
        0x21f8, 0x71ec, 0xf9ec, 0xfcfc,
        0xbe7e, 0x4c81, 0x717e, 0x4082,
        0x307c, 0x0f80, 0x0000, 0x0000]

def random(a,b):                                                            
    result = uos.urandom(1)[0]                                              
    result /= 256                                                           
    result *= b-a                                                           
    result += a                                                             
    return int(result)

def cls():
    oled.fill(0)
    oled.show()

def sprite(bitmap, x=0, y=0):
    height = len(bitmap)
    width = len(bin(max(bitmap))) - 2
    fbuf = framebuf.FrameBuffer(bytearray(width*height//8),
                                width,height,framebuf.MVLSB)
    formatter = '%0' + str(width) + 'd'
    for line, i in enumerate(bitmap):
        bitline = formatter % int(bin(i)[2:])
        for column, j in enumerate(bitline):
            fbuf.pixel(x + column, y + line, int(j))
    return fbuf

fbird = sprite(bird)

up = framebuf.FrameBuffer(bytearray(16*32//8),
                          16,32,framebuf.MVLSB)
up.rect(2,0,12,27,1)
up.rect(0,26,16,6,1)

down = framebuf.FrameBuffer(bytearray(16*32//8),
                          16,32,framebuf.MVLSB)                         
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
    if y < 0:
        y = 0
        vel = 0
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
    oled.framebuf.blit(fbird, 0, round(y))
    oled.framebuf.blit(up,x_tower1,y_tower1-46)
    oled.framebuf.blit(down,x_tower1,y_tower1+18)
    oled.framebuf.blit(up,x_tower2,y_tower2-46)
    oled.framebuf.blit(down,x_tower2,y_tower2+18)
    oled.show()