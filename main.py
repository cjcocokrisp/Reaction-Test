# Timing Test game developed with Python and the module Pygame.
# More information about Pygame can be found at https://www.pygame.org/news.

import pygame as pg
from settings import *
from sprites import *

class Game:

    "The class that manages the games functions."

    def __init__(self):
        self.running = True
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Timing Test")
        self.font_name = pg.font.match_font(FONT_NAME)
        self.clock = pg.time.Clock()
        self.playing = False
        self.round = 1
        self.scores = []
        self.finalScore = 0
        self.complete = False

    def new(self):
        
        "Creates the sprite groups and adds the sprites to the screen and then runs the main loop."

        self.all_sprites = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.square = Square(0, HEIGHT / 2 - 25) # The height is subtracted by 25 to have the center of the square be in the middle.
                                                 # The (x,y) coordinates of the sprite are in the top left corner.
        # Instead of defining each indivual background elements they are stored in a list in settings.py and then added to the background sprite group. 
        for back in BACKGROUNDS: 
            b = Backgrounds(*back)
            self.all_sprites.add(b)
            self.background.add(b)
        self.all_sprites.add(self.square) # The square is added to the all sprites group here so it is above the background elements.
        self.run()

    def run(self):
        
        "Runs the main parts of the main loop which include events, update, draw."

        # The amount of rounds that are played is 3 so when the main loop is ran it checks to see if the round is correct.
        if self.round < 4:
            self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        
        "Updates the sprites that are on the screen and responds to user input."

        self.all_sprites.update()
        
        # For explanation on why the rightCount is used see sprites.py.
        if self.square.pressed:
            if self.square.rect.x > 500:
                self.scores.append(self.square.rightCount * 2) 
            else:
                self.scores.append(self.square.rect.x * 2)
            
            self.playing = False   



    def events(self):
        
        "Defines the events that can occur during the main loop which include exiting the program."

        # Quits the program if any of these events are triggered.
        for event in pg.event.get():
            if event.type == pg.QUIT: # pg.QUIT is the X on the title bar of the window.
                self.running = False
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.playing = False


    def draw(self):
        
        "Draws the objects to the screen during the main loop."

        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def start_screen(self):

        "Displays the start screen with instructions on how to play."

        self.screen.fill(WHITE)
        self.draw_text("Timing Test", 36, BLACK, WIDTH / 2, 110)
        self.draw_text("Click the space bar when the square reaches enters the green area.", 24, BLACK, WIDTH / 2, 165)
        self.draw_text("Click the any key to continue...", 24, BLACK, WIDTH / 2, 300)
        pg.display.flip()
        self.wait_for_input()

    def score_screen(self):
        
        "Displays the score of the round that was just played."

        self.screen.fill(WHITE)
        # Only displays the score between rounds if the round is 1, 2, or 3.
        if self.round < 4:
            self.draw_text("Round " + str(self.round) + " Score:" + str(self.scores[self.round - 1]), 64, BLACK, WIDTH / 2, HEIGHT / 3)
        pg.display.flip()
        pg.time.wait(2000)
        self.round += 1
        # Continues the main loop if the round is 1, 2, or 3. 
        # After round 3 it will display the final score and instructions on what to do next.
        if self.round < 4:
            self.playing = True
            self.square.reset()
            self.square.pressed = False
        else:
            self.finalScore = self.scores[0] + self.scores[1] + self.scores [2]
            self.complete = True
            self.square.reset()

    def results_screen(self):

        "Displays the results screen that shows the final score as well as instructions on how to play again or quit."

        self.screen.fill(WHITE)
        self.draw_text("Good job! Your final score was " + str(self.finalScore) + " points!", 48  , BLACK, WIDTH / 2, 125)
        self.draw_text("Click escape to quit or space to play again.", 48, BLACK, WIDTH / 2, 225)
        pg.display.flip()
        self.wait_for_input()

    def wait_for_input(self):

        "Freezes all action and waits for the user to make an input. Used on the title screen and results screen."

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    self.playing = False
                if event.type == pg.KEYUP:
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.waiting = False
                        self.running = False
                        self.playing = False
                    # Resets the program after pressing space on the title or final results screen to insure that things run properly.
                    if event.key == pg.K_SPACE:
                        self.complete = False
                        self.playing = True
                        self.round = 1
                        self.scores = []



    def draw_text(self, text, size, color, x, y):
        
        """ Draws the text """ 
       
        font = pg.font.Font(self.font_name, size) # Checks to see if the font is part of Pygame's font library. 
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.start_screen()
while game.running:
    game.new()
    if not game.playing:
        game.score_screen()
    if game.complete:
        game.results_screen()

