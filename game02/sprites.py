# content from kids can code: http://kidscancode.org/blog/'
# https://github.com/kidscancode/pygame_tutorials/tree/master/platform
# other sources: Chris Cozort

# import moudles and libraries
from typing import Any
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os
from math import *
from settings import *
from random import randint


# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images02')
snd_folder = os.path.join(game_folder, 'sounds02')

# sprite that the character shoots
class Bullet(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # uses an image
        self.image = pg.image.load(os.path.join(img_folder, 'pew.png')).convert()
        # if there are black pixels, don't draw them
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # spawn at the player's position and a bit down and forward to make it come out of the front nose of the player image
        self.pos = vec(PLAYER_POS) - vec(-30, 20)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):
        # speed at which the bullet will move
        self.acc = vec(5,0)
        # equations of motion
        self.acc.x += self.vel.x * -PLAYER_FRIC/2
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # if bullet goes off screen, stop loading it
        if self.rect.left < 0:
            pg.sprite.Sprite.kill(self)
        if self.rect.bottom > HEIGHT:
            pg.sprite.Sprite.kill(self)
        if self.rect.top < 0:
            pg.sprite.Sprite.kill(self)
        if self.rect.right > WIDTH:
            pg.sprite.Sprite.kill(self)    

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'f15.png')).convert()
        # if there are white pixels, don't draw them
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 10)
        # spawns player on the left side of the screen
        self.pos = vec(WIDTH/2 - 200, HEIGHT/2 + 100)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
        # this variable will be used to make the enemies track the player
        global PLAYER_POS
        PLAYER_POS = self.pos
    # controls
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_w]:
            self.acc.y = -5
        if keys[pg.K_s]:
            self.acc.y = 5
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.acc.y += self.vel.y * -PLAYER_FRIC
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # prevents player from going off screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        

class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind, speed):
        Sprite.__init__(self)
        self.game = game
        self.kind = kind
        self.speed = speed
        self.image = pg.Surface((w, h))
        self.image = pg.image.load(os.path.join(img_folder, 'rocket.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(WIDTH/2, HEIGHT/2)
    def update(self):
        if self.kind == "normal":
            self.rect.x -= self.speed
        if self.kind == "attack":
            # variable which will be used to change the velocity of the enemy sprite
            mobspeedy = 2
            mobspeedx = 2
            if self.pos.y > HEIGHT or self.pos.y < 0:
                self.rect.y += mobspeedy
                mobspeedy = -mobspeedy
            # if the enemy is to the left of the player, keep moving forward
            if self.game.player.rect.x > self.rect.x:
                self.rect.x -= mobspeedx
                mobspeedx += 1
            # if the enemy is to the right of the player, change it's y value to try to hit the player
            if self.game.player.rect.x < self.rect.x:
                self.rect.x -= mobspeedx
                mobspeedx += 1
                if self.game.player.rect.y > self.rect.y:
                    self.rect.y += mobspeedy
                    mobspeedy += 1
                if self.game.player.rect.y < self.rect.y:
                    self.rect.y -= mobspeedy
                    mobspeedy += 1
        
        # if the enemy goes off screen, the player loses a point - rewards player for shooting the enemies and not dodging them
        if self.rect.left < 0:
            pg.sprite.Sprite.kill(self)
            self.game.hitpoints += -1
        if self.rect.bottom > HEIGHT:
            pg.sprite.Sprite.kill(self)
            self.game.hitpoints += -1
        if self.rect.top < 0:
            pg.sprite.Sprite.kill(self)
            self.game.hitpoints += -1
        