# The file was created by Jason Liau

# This asterisk is pulling information from the settings file - We are also importing modules we will access later
import pygame as pg
from settings import *
# Allows us to use random elements
from random import randint
# Allows us to use information from sprites
from sprites import *
# Imports the sys module (gives access to windows so we can close the window)
import sys
# Imports the operating system
from os import path
  
# This creates a "mold" for our game - Game blueprint
class Game:
    # Initializes the game
    def __init__(self):
        # Initializer -- initializes pygame and settings - Contains information about the game
        pg.init()
        # Settings - What different settings affect
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock
        self.clock = pg.time.Clock()
        # Allows us to store information and set highscores
        self.load_data()
        # defines the load data method
    def load_data(self):
        game_folder = path.dirname(__file__)
        # empty list for map data
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        # Allows us to access/make the map
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                # prints the map
                print(line)
                self.map_data.append(line)

    def new(self):
        # creates sprite group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # This puts the player in the middle of the screen and allows it to have access to the rest of the game (such as walls)
        # # this is a class because it has a capital G
        # # Adds player1 to the class
        # self.all_sprites.add(self.player1)
        # # creates a wall that has an x value between 10 and 20 and a y value of 5
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        # Creates a list out of our map data
        for row, tiles in enumerate(self.map_data):
            # prints each item in the list (prints our map)
            print(row)
            # prints our collumns
            for col, tile in enumerate(tiles):
                print(col)
                # places a wall where we mark 1 in map.txt
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                    # places the player where we mark P in map.txt
                if tile == "P":
                    self.player1 = Player(self, row, col)
                # if tile == "p":
                #     self.player2 = Player(self, row, col)

    # Runs our game - Starts game
    def run(self):
        # Makes it true that we are playing the game
        self.playing = True
        while self.playing:
            # tick speed
            self.dt = self.clock.tick(FPS) / 1000
            # calling other modules
            # allows us to move left, right, up, and down with the direction keys
            self.events()
            # updates other sprites
            self.update()
            # draws sprites, grid, and sprites
            self.draw()

    def quit(self):
        # quits pygame
         pg.quit()
        #  exits the system window
         sys.exit()
        

    def update(self):
        # This runs everything update (enemies march, powerups bob up and down)
        self.all_sprites.update()

    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
             # Tuples are the parenthesees - they are lists that don't change
             pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
             # Tuples are the parenthesees - they are lists that don't change
             pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
        # gives us the ability to draw the sprites
    def draw(self):
            # fills the background color
            self.screen.fill(BGCOLOR)
            # draws the grid
            self.draw_grid()
            # draws the sprites on the screen
            self.all_sprites.draw(self.screen)
            # prepares memory to accept next frame
            pg.display.flip()

    def events(self):
        for event in pg.event.get():
            # Quit the game if the event is quit pygame
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     # Makes it so that the character moves when the left button is pressed
            #     if event.key == pg.K_LEFT:
            #         # Moves the player left by 1
            #         self.player1.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         # Moves the player right by 1
            #         self.player1.move(dx=1)
            #     if event.key == pg.K_UP:
            #         # Moves the player up by 1
            #         self.player1.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         # Moves the player down by 1
            #         self.player1.move(dy=1)

# Create a new game
g = Game()
# g.show_start_screen()
while True:
    # create new game
    g.new()
    # run the game
    g.run()
    # g.show_go_screen()