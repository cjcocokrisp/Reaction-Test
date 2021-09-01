import pygame as pg 
from settings import *

vec = pg.math.Vector2

class Square(pg.sprite.Sprite):

    "Class that manages the square the player will stop to be scored."

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 0  # 0 = Right 
                            # 1 = Left 
                            # 2 = Stopped
        self.moving = True
        self.pressed = False
        self.side = 0 # 0 = Left Side of Screen 
                      # 1 = Right Side of Screen
        self.rightCount = 500

    def reset(self):
        
        "Resets the square to it's orginal state."

        self.rect.x = 0
        self.rightCount = 500
    
    def update(self):
        
        "Updates the squares position to keep score."

        keys = pg.key.get_pressed()

        if not self.pressed:
            if keys[pg.K_SPACE]:
                self.direction = 2
                self.pressed = True
                
            
        if self.direction == 0:
            self.rect.x += 25
            if self.rect.x == 1000:
                self.direction = 1
        elif self.direction == 1:
            self.rect.x -= 25
            if self.rect.x == 0:
                self.direction = 0
        
        # Checks to see which side of the screen that the square is on.
        if self.rect.x > 500:
            self.side = 1
        else:
            self.side = 0
            self.rightCount = 500

        # If the square is on the right side of the screen it counts where so scoring can be equal.
        if self.side == 1:
            if self.direction == 0:
                self.rightCount -= 25
            elif self.direction == 1:
                self.rightCount += 25
            

class Backgrounds(pg.sprite.Sprite):

    "Class that manages the background elements of the program."

    def __init__(self, x, y, width, height, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

