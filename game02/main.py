# content from kids can code: http://kidscancode.org/blog/'
# https://github.com/kidscancode/pygame_tutorials/tree/master/platform
# other sources: Chris Cozort
# sound effects from mixkit

# My goals
# create a player that can shoot bullets at an enemy - yes
# create a enemy that tries to attack the player - kinda
# death animation and sound effects - yes sound effects
# score function - yes

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
from random import randint
import os
from math import *
from settings import *
from sprites import *
vec = pg.math.Vector2
import time

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images02')
snd_folder = os.path.join(game_folder, 'sounds02')

# create a class which will be used a clock
class Cooldown():
        def __init__(self):
            self.current_time = 0
            self.event_time = 0
            self.delta = 0
        def ticking(self):
            self.current_time = (pg.time.get_ticks())/1000
            self.delta = self.current_time - self.event_time
        def timer(self):
            self.current_time = (pg.time.get_ticks())/1000

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        # sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Missle Defender")
        # create a clock inside pygame
        self.clock = pg.time.Clock()
        self.running = True
        # begin running the clock
        self.cd = Cooldown()
    
    def new(self):
        # variable to be used to show the end screen
        self.game_over = False
        # sets a wre variable
        self.hitpoints = 20
        # this variable will be used to make the game harder as you progress
        self.level = 0
        # create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_bullets = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
        # music
        pg.mixer.music.load(os.path.join(snd_folder, 'play.wav'))
        pg.mixer.music.set_volume(1)
        # loops the music
        pg.mixer.music.play(-1)
        # runs the class run
        self.run()
    
    # what happens while the game runs
    def run(self):
        self.playing = True
        # spawns the first mobs
        self.mob_spawn()
        # the game loop
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        # begin ticking the clock
        self.cd.ticking()
        # update all the sprites on screen
        self.all_sprites.update()
        # print(f"current time: {self.cd.current_time} button press time: {self.cd.event_time} delta time {self.cd.delta}")
        # if the enemies collide with a bullet, they die and you get 1 point
        pg.sprite.groupcollide(self.all_bullets, self.all_mobs, True, True)
        # if there are 0 mobs on the screen, spawn more and make the diffuclty harder
        if len(self.all_mobs) == 0:
            self.mob_spawn()
            self.level += 1

    # events that can happen
    def events(self):
        # quit
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        # see if player wants to shoot 
        self.shoot()
        # if the player collides with a mob its game over
        if pg.sprite.spritecollide(self.player, self.all_mobs, True, pg.sprite.collide_rect_ratio(0.5)):
            pg.sprite.Sprite.kill(self.player)
            self.game_over = True
        # if 20 missles get past the player, game over
        if self.hitpoints == 0:
            self.game_over = True

    # shoot function
    def shoot(self):
        # if the player presses space and the timer has been running for more than 0.3 seconds, create a bullet and shoot it
        if pg.key.get_pressed()[pg.K_SPACE] and self.cd.delta > 0.3:
            self.cd.event_time = pg.time.get_ticks()/1000
            b = Bullet()
            self.all_sprites.add(b)
            self.all_bullets.add(b)
            # sound effect
            pg.mixer.Channel(1).play(pg.mixer.Sound(os.path.join(snd_folder, 'pew.wav')))
        
    # function that spwans the mobs - used in respawing them too
    def mob_spawn(self):
        for m in range(0 + self.level):
            m = Mob(self, (WIDTH - 30), randint(20, (HEIGHT - 20)), 20, 20, "normal", randint(1, 4))
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        
        # mob that tracks the player and tries to hit them
        if self.level > 4:
            for m in range(floor(self.level/4)):
                m = Mob(self, (WIDTH - 30), randint(20, (HEIGHT - 20)), 20, 20, "attack", randint(1,2))
                self.all_sprites.add(m)
                self.all_mobs.add(m)
    
    # function that draws everything on screen
    def draw(self):
        if self.game_over == False:
            # draw the background screen
            self.screen.fill(BLUE)
            # draw all sprites
            self.all_sprites.draw(self.screen)
            self.draw_text("Hitpoints: " + str(self.hitpoints), 22, WHITE, WIDTH/2, HEIGHT/10 - 30)
            self.draw_text("Level: " + str(self.level - 1), 22, WHITE, WIDTH/2, (HEIGHT/10 - 10))
            # buffer - after drawing everything, flip display
            pg.display.flip()
        # if the player collides with an enemy:
        if self.game_over == True:
            # like in mario where the screen freezes for a bit
            time.sleep(1)
            # clear screen
            self.screen.fill(BLUE)
            # sound that plays when you die
            pg.mixer.music.load(os.path.join(snd_folder, 'die.wav'))
            pg.mixer.music.set_volume(1)
            pg.mixer.music.play()
            # game over text
            self.draw_text("GAME OVER!", 64, WHITE, WIDTH / 2, HEIGHT / 3)
            pg.display.flip()
            time.sleep(1)
            pg.display.quit() 
            
    # function that makes writing text on the screen much easier
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('impact')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

# runs the game
g = Game()
while g.running:
    g.new()

pg.quit()
