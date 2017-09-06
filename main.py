'''
Flappy Bird for ESP8266 modules
github.com/zelacerda/micropython

Version 1.0
2017 - by zelacerda
'''

import ssd1306
from framebuf import FrameBuffer as FB
from machine import I2C, Pin

# Screen dimensions
WIDTH = 128
HEIGHT = 64

# Initialize pins
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(13, Pin.IN)

# Some helper functions
def random(a,b):
    result = uos.urandom(1)[0] / 256
    result *= b-a
    result += a
    return int(result)

def to_bytearray(s):
    return bytearray([int('0x'+s[i:i+2]) for i in range(0,len(s),2)])

# Bitmap images
BIRD = '07e018f021f871ecf9ecfcfcbe7e4c81717e4082307c0f80'
COL1 = '200c'*26+'ffff'+'8007'*4+'ffff'
COL2 = 'ffff'+'8007'*4+'ffff'+'200c'*26
bird_size = (16,12)
colu_size  = (16,32)

# Generate sprites
bird = FB(to_bytearray(BIRD),bird_size[0],bird_size[1],3)
col1 = FB(to_bytearray(COL1),colu_size[0],colu_size[1],3)
col2 = FB(to_bytearray(COL2),colu_size[0],colu_size[1],3)

class FlappyBird:
    def __init__(self):
        self.height = bird_size[1]
        self.y = HEIGHT // 2 - self.height // 2
        self.vel = -wing_power
    
    def move(self):
        self.vel += gravity
        self.y = int(self.y + self.vel)
        
    def crashed(self):
        y_limit = HEIGHT - self.height
        return self.y > y_limit
            
    def flap(self):
        self.vel = -wing_power

class Obstacle:
    def __init__(self, x):
        self.gap = random(6+gap_size, HEIGHT-6-gap_size) 
        self.x = x
        self.score = 0
        
    def scroll(self):
        self.x -= velocity
        if self.x < -colu_size[0]:
            self.score += 1
            self.x = WIDTH
            self.gap = random(6+gap_size, HEIGHT-6-gap_size)

def clicked():
    global pressed
    if button.value() == 1 and not pressed:
        pressed = True
        return True
    elif button.value() == 0 and pressed:
        pressed = False
    return False

def draw():
    oled.fill(0)
    oled.framebuf.blit(bird, 0, flappy_bird.y)
    oled.framebuf.blit(col1,obstacle_1.x,obstacle_1.gap-gap_size-colu_size[1])
    oled.framebuf.blit(col2,obstacle_1.x,obstacle_1.gap+gap_size)
    oled.framebuf.blit(col1,obstacle_2.x,obstacle_2.gap-gap_size-colu_size[1])
    oled.framebuf.blit(col2,obstacle_2.x,obstacle_2.gap+gap_size)
    oled.text(str(obstacle_1.score + obstacle_2.score), WIDTH//2 - 8, 0)
    oled.show()

# Game parameters
gap_size   = 15
velocity   = 3
gravity    = .6
wing_power = 4
state = 0
pressed = False

# Game state functions
def splash_screen():
    global state
    oled.fill(0)
    oled.text('F L A P P Y', 20, 20)
    oled.text('B I R D', 36, 40)
    oled.show()
    if clicked(): state = 1

def game_start():
    global state,score,flappy_bird,obstacle_1,obstacle_2, pressed
    flappy_bird = FlappyBird()
    obstacle_1 = Obstacle(WIDTH)
    obstacle_2 = Obstacle(WIDTH + (WIDTH + colu_size[0]) // 2)
    state = 2

def game_running():
    global state
    if clicked(): flappy_bird.flap()
    flappy_bird.move()
    if flappy_bird.crashed(): state = 3
    obstacle_1.scroll()
    obstacle_2.scroll()
    draw()
    
def game_over():
    global state
    oled.framebuf.fill_rect(20, 10, 88, 44, 0)
    oled.framebuf.rect(20, 10, 88, 44, 1)
    oled.text('G A M E', 36, 20)
    oled.text('O V E R', 36, 36)
    oled.show()
    if clicked(): state = 1

def loop():
    while True:
        if   state == 0: splash_screen()
        elif state == 1: game_start()
        elif state == 2: game_running()
        elif state == 3: game_over()
        
loop()