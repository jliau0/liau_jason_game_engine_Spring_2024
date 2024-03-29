# This file was created by: Jason Liau
# This code was inspired by Zelda and informed by Chris Bradfield

# allows us to use pygame and imports game settings
import pygame as pg
from settings import *

# testing github upload

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
        # sets the player image
        self.image = game.player_img
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
        self.moneybag = 0
        # allows us to access speed conveniently
        self.speed = 301
        self.moneybag = 0
        self.hitpoints = 1

    # allows us to access keyboard inputs
    def get_keys(self):
        # sets the velocity for the x and y direction to 0
        self.vx, self.vy = 0, 0
        # makes our character move when a key is pressed
        keys = pg.key.get_pressed()
        # Makes the character move left (have less speed) when the left arrow or the a key is pressed
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        # Makes the character move right (have more speed) when the right arrow or the d key is pressed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed 
        # Makes the character move up (have less speed because y is counted from top to bottom)
        # when the up arrow or the w key is pressed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed 
        # Makes the character move down (have more speed because y is counted from top to bottom) 
        # when the down arrow or the s key is pressed 
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
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
            # hits are collisions
            if hits:
                if self.vx > 0:
                # If the velocity in the x direction is positive and the objects collide, we must subtract the width of
                # the rectangle because the contact point is in the upper left corner
                    self.x = hits[0].rect.left - self.rect.width
                # creates collions in the x direction for a negative velocity
                if self.vx < 0:
                    self.x = hits[0].rect.right
                # resets velocity and rectangle
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
            # resets velocity and rectangle
                self.vy = 0
                self.rect.y = self.y
                
        # Allows us to collide with coins and have them dissappear
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        # hits is equal to collisions
        if hits:
            return True
        # return true when we hit a coin

    # made possible by Aayush's question
    # Creates a method for the collision
    # Kill determines whether the coin disappears
    def collide_with_group(self, group, kill):
        # sets collision for groups
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                # adds a coin to the moneybag when we contact a coin
                self.moneybag += 1
                # allows us to do things based on when we collide with a powerup
            if str(hits[0].__class__.__name__) == "PowerUp":
                # makes us faster when we hit a powerup
                self.speed += 150
            if str(hits[0].__class__.__name__) == "SpeedDown":
                # makes us slower when we hit a speed down powerup
                self.speed -= 150
            if str(hits[0].__class__.__name__) == "Mob":
                # reduces our hitpoints when we contact a mob
                print("Collided with mob")
                self.hitpoints -= 1
            if str(hits[0].__class__.__name__) == "SuperMob":
                # reduces our hitpoints when we contact a super mob
                print("Collided with super mob")
                self.hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Shield":
                # adds hitpoints when we hit a shield powerup
                self.hitpoints += 10

    def update(self):
        # gives access to keyboard inputs
        self.get_keys()
        # controls player's speed in x and y direction
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # determines where the rectangle is on the screen
        self.rect.x = self.x
        # add collision
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision
        self.collide_with_walls('y')
        # calls the collide with group method
        self.collide_with_group(self.game.coins, True)
        # adds collision for powerups
        self.collide_with_group(self.game.power_ups, True)
        # adds collision for speed down powerups
        self.collide_with_group(self.game.speed_down, True)
        # adds collision for mobs
        self.collide_with_group(self.game.mobs, False)
        # adds collision for super mobs
        self.collide_with_group(self.game.super_mobs, False)
        # adds collision for invincibility powerup
        self.collide_with_group(self.game.shield, True)

        # adds actions based on our moneybag count and hitpoint value
        if self.moneybag == 11:
            # prints you win and shows victory screen when we collect 10 coins
            print("You win!")
            self.game.show_victory_screen()
        if self.hitpoints <= 0:
            # prints you suck and shows loss screen when our hitpoints is 0 or negative
            print("You suck")
            self.game.show_loss_screen()

        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")

        # adds money to our moneybag when we collide with a coin (not currently displaying moneybag)
        # if self.collide_with_group(self.game.coins, True):
        #     self.moneybag += 1
      

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

# creates new coin class
class Coin(pg.sprite.Sprite):
    # initializes the class
    def __init__(self, game, x, y):
        # adds the sprite to the all sprites group and to the coins group
        self.groups = game.all_sprites, game.coins
        # initializes the class
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets the coin class game equal to the game
        self.game = game
        # sets the coin image
        self.image = game.coin_img
        # allows us to get the rectangle
        self.rect = self.image.get_rect()
        # sets the x and y coordinates of the coin
        self.x = x
        self.y = y
        # sets the position and size of the coin
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
# creates new powerup class
class PowerUp(pg.sprite.Sprite):
    # initializes the class
    def __init__(self, game, x, y):
        # adds the sprite to the all sprites group and to the power up group
        self.groups = game.all_sprites, game.power_ups
        # initializes the class
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets the power up class game equal to the game
        self.game = game
        # sets the power up image
        self.image = game.speedUp_img
        # allows us to get the rectangle
        self.rect = self.image.get_rect()
        # sets the x and y coordinates of the power up
        self.x = x
        self.y = y
        # sets the position and size of the power up
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# creates new powerup class
class SpeedDown(pg.sprite.Sprite):
    # initializes the class
    def __init__(self, game, x, y):
        # adds the sprite to the all sprites group and to the power up group
        self.groups = game.all_sprites, game.speed_down
        # initializes the class
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets the power up class game equal to the game
        self.game = game
        # sets the power up image
        self.image = game.slowDown_img
        # allows us to get the rectangle
        self.rect = self.image.get_rect()
        # sets the x and y coordinates of the power up
        self.x = x
        self.y = y
        # sets the position and size of the power up
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# creates new powerup class
class Shield(pg.sprite.Sprite):
    # initializes the class
    def __init__(self, game, x, y):
        # adds the sprite to the all sprites group and to the power up group
        self.groups = game.all_sprites, game.shield
        # initializes the class
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets the shield class game equal to the game
        self.game = game
        # sets the shield image
        self.image = game.shield_img
        # allows us to get the rectangle
        self.rect = self.image.get_rect()
        # sets the x and y coordinates of the shield power up
        self.x = x
        self.y = y
        # sets the position and size of the shield power up
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# makes mob class
class Mob(pg.sprite.Sprite):
    # instantiates mob
    def __init__(self, game, x, y):
        # adds mob to all sprites and mobs
        self.groups = game.all_sprites, game.mobs
        # initializes the mob and groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # sets appearance of the mob as an image
        self.image = game.mob_img
        # sets the rectangle and position of rectangle for the mob
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # sets the speed of the mob
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        # sets collision with walls for the mob
    def collide_with_walls(self, dir):
        # sets collision with walls in the x-direction
        if dir == 'x':
            # print('colliding on the x')
            # makes it so that the wall does not disappear when we contact it
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # adjusts velocity when we contact a wall
            if hits:
                self.vx *= -1
                self.rect.x = self.x
                # sets collision for the y direction
        if dir == 'y':
            # print('colliding on the y')
            # makes it so that the wall does not disappear when we contact it
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # adjusts velocity when we contact wall
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        # controls velocity and position
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        # makes our velocity depend on the player's velocity and position so that we follow it
        if self.rect.x < self.game.player1.rect.x:
            self.vx = 200
        if self.rect.x > self.game.player1.rect.x:
            self.vx = -200    
        if self.rect.y < self.game.player1.rect.y:
            self.vy = 200
        if self.rect.y > self.game.player1.rect.y:
            self.vy = -200
        # codes collision with walls
        # disables collision with walls
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class SuperMob(pg.sprite.Sprite):
    # instantiates mob
    def __init__(self, game, x, y):
        # adds super mob to all sprites and mobs
        self.groups = game.all_sprites, game.super_mobs
        # initializes the mob and groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # sets appearance of the mob as an image
        self.image = game.supermob_img
        # sets the rectangle and position of rectangle for the mob
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # sets the speed of the mob
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        # sets collision with walls for the mob
    def collide_with_walls(self, dir):
        # sets collision with walls in the x-direction
        if dir == 'x':
            # print('colliding on the x')
            # makes it so that the wall does not disappear when we contact it
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # adjusts velocity when we contact a wall
            if hits:
                self.vx *= -1
                self.rect.x = self.x
                # sets collision for the y direction
        if dir == 'y':
            # print('colliding on the y')
            # makes it so that the wall does not disappear when we contact it
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # adjusts velocity when we contact wall
            if hits:
                self.vy *= -1
                self.rect.y = self.y

    def update(self):
        # self.rect.x += 1
        # controls velocity and position
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        # makes our velocity depend on the player's velocity and position so that we follow it
        if self.rect.x < self.game.player1.rect.x:
            self.vx = 150
        if self.rect.x > self.game.player1.rect.x:
            self.vx = -150    
        if self.rect.y < self.game.player1.rect.y:
            self.vy = 150
        if self.rect.y > self.game.player1.rect.y:
            self.vy = -150
        # codes collision with walls
        # disables collision with walls
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')



