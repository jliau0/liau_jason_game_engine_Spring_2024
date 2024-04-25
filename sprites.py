# This file was created by: Jason Liau
# This code was inspired by Zelda and informed by Chris Bradfield

# allows us to use pygame and imports game settings
import pygame as pg
from settings import *
from os import path

SPRITESHEET = "theBell.png"

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')


# allows us to use multiple images from a file
class Spritesheet:
    # allows us to use the images from our spritesheet
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # pull an image from a larger spreadsheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width, height))
        # Gives us the iamge that we want to pull from the spritesheet
        return image
    

# class Animated_sprite(Sprite):
#     def __init__(self):
#         Sprite.__init__(self)
#         self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
#         self.load_images()
#         self.image = self.standing_frames[0]
#         self.rect = self.image.get_rect()
#         self.current_frame = 0
#         self.last_update = 0
        
    # def load_images(self):
    #     self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
    #                             self.spritesheet.get_image(32, 0, 32, 32)]
    #     for frame in self.standing_frames:
    #         frame.set_colorkey(BLACK)
    #     self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
    #                           self.spritesheet.get_image(692, 1458, 120, 207)]
    #     self.walk_frames_l = []
    #     for frame in self.walk_frames_r:
    #         frame.set_colorkey(BLACK)
    #         self.walk_frames_l.append(pg.transform.flip(frame, True, False))
    #     self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
    #     self.jump_frame.set_colorkey(BLACK)
    # def update(self):
    #     self.animate()


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
        self.spritesheet = Spritesheet(path.join(img_dir, 'theBell.png'))
        self.load_images()
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
        self.speed = 50
        self.moneybag = 0
        self.hitpoints = 1
        self.current_frame = 0
        self.last_update = 0
        self.speed_powerups = 0
        self.shield_powerups = 0
        self.jumping = False
        self.walking = False
        # sets up a cooldown for our powerups
        self.powered_up = False
        # controls cooldown length
        self.powerup_cooldown = 1
        self.powerup_timer = self.powerup_cooldown

    # allows us to access keyboard inputs
    def get_keys(self):
        # creates a cooldown when we are powered up
        if self.powered_up:
            self.powerup_timer -= self.game.dt
            if self.powerup_timer <= 0:
                self.powerup_timer = self.powerup_cooldown
                self.powered_up = False
            # not powered up after 1 second
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
        if keys[pg.K_e] and self.speed_powerups >= 1 and self.powered_up == False:
            # increases speed if we have one or more speed powerups and we press the e key
            self.powered_up = True
            self.speed += 300
            self.speed_powerups -= 1
        if keys[pg.K_q] and self.shield_powerups >= 1 and self.powered_up == False:
            # increases health if we have one or more shield powerups and we press the q key
            self.powered_up = True
            self.hitpoints += 10
            self.shield_powerups -= 1


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

    # accesses images for animation
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]

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
                self.speed_powerups += 1
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
                self.shield_powerups += 1
            if str(hits[0].__class__.__name__) == "BossMob":
                # adds hitpoints when we hit a shield powerup
                self.hitpoints -= 10

    # Animates our sprite based on the time
    def animate(self):
        now = pg.time.get_ticks()
        # sets the frames based on our state
        if not self.jumping and not self.walking:
            if now - self.last_update > 500:
                self.last_update = now
                # accesses the frame that we are on
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                # sets image position and current image
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

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
        # adds collision for shield powerup
        self.collide_with_group(self.game.shield, True)
        # adds collision for boss mob
        self.collide_with_group(self.game.boss_mobs, False)

        ## adds actions based on our moneybag count and hitpoint value and level (help from Aayush)
        if self.moneybag == 100 and self.game.current_level == 'LEVEL5':
            # prints you win and shows victory screen when we collect 11 coins on the final level
            print("You win!")
            self.game.show_victory_screen()
        if self.hitpoints <= 0:
            # prints you suck and shows loss screen when our hitpoints is 0 or negative
            print("You suck")
            self.game.show_loss_screen()

        # updates our animation
        self.animate()

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

class BossMob(pg.sprite.Sprite):
    # instantiates boss mob
    def __init__(self, game, x, y):
        # adds super mob to all sprites and mobs
        self.groups = game.all_sprites, game.boss_mobs
        # initializes the mob and groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # sets appearance of the mob as an image
        self.image = game.bossmob_img
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
            # print('colliding on the 'y')
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
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')





