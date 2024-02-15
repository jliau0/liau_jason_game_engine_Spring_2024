# This file was created by: Jason Liau
# This code was inspired by Zelda and informed by Chris Bradfield

# allows us to use pygame and imports game settings
import pygame as pg
from settings import *


# Create a "mold" for the player - Inherits from pg.sprite.Sprite - Subclass of pg.sprite.Sprite
class Player(pg.sprite.Sprite):
    # initializes the player class
    def __init__(self, game, x, y):
        # this makes the player part of all sprites
        self.groups = game.all_sprites
        # initialize super class (mammel - monkey, giraffe, human) Mammel is superclass - Human is subclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # Allows player to have access to the game information
        self.game = game
        # makes dimenensions for self.image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # fills self.image with green color
        self.image.fill(GREEN)
        # gives size and position of the rectangle
        self.rect = self.image.get_rect()
        # establishes x-coordinate of player
        # self.x = x
        # # establishes y-coordinate of player
        # self.y = y
        # sets the velocity for x and y direction to 0
        self.vx, self.vy = 0, 0
        # Sets the player's position
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    # allows us to access keyboard inputs
    def get_keys(self):
        # sets the velocity for the x and y direction to 0
        self.vx, self.vy = 0, 0
        # makes our character move when a key is pressed
        keys = pg.key.get_pressed()
        # Makes the character move left (have less speed) when the left arrow or the a key is pressed
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED  
        # Makes the character move right (have more speed) when the right arrow or the d key is pressed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED 
        # Makes the character move up (have less speed because y is counted from top to bottom)
        # when the up arrow or the w key is pressed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED 
        # Makes the character move down (have more speed because y is counted from top to bottom) 
        # when the down arrow or the s key is pressed 
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        # This makes it so that we do not travel faster in the diagonal direction according to pythagoras' 
        # formula because the hypotanuse of a triangle is more direct than traveling the x and y distances
        if self.vx != 0 and self.vy != 0:
            # makes it slower to travel along the hypotanuse
            self.vx *= 0.7071
            self.vy *= 0.7071


    # This tells it how far to move from itself so it should move then stop
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
            
    # Allows us to collide with walls and not move through them
    def collide_with_walls(self, dir):
        # If it hits in the x-direction
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                # If the velocity in the x direction is positive and the objects collide, we must subtract the width of
                # the rectangle because the contact point is in the upper left corner
                    self.x = hits[0].rect.left - self.rect.width
                # creates collions in the x direction for a negative velocity
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        # If the collision occurs in the y-direction
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
            # If the block is moving down (velocity in the y direction is positive because y is counted top to bottom)
                if self.vy > 0:
            # Same situation- Must subtract height because contact point is in the top left of the screen
                    self.y = hits[0].rect.top - self.rect.height
             # Codes collision for the y direction moving upward
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # placeholder to control the sprite's behavior
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # determines where the rectangle is on the screen
        self.rect.x = self.x
        # add collision
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')

# sprite = module Sprite = class (Uppercase)
# creates mold for wall
class Wall(pg.sprite.Sprite):
    # initializes the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        # initialize superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # sets the size of the wall
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # sets color of wall
        self.image.fill(BLUE)
        # returns size and position of the rectangle (wall)
        self.rect = self.image.get_rect()
        # sets x and y coordinates for wall
        self.x = x
        self.y = y 
        # determines where wall will be placed
        self.rect.x = x *  TILESIZE
        self.rect.y = y *  TILESIZE




