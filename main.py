#! python3.8

"""
=================================================
Title: Tilemap Test
About: Trying out PyGame's Tilemap functionality
Author: Brandon "Bearheathen" Stewart
Deps: Pygame 1.9.6, settings.py, sprites.py
Copyright: 2020

=================================================

"""
import sys
from os import path

from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250, 100)  # <<- delay time, how often to repeat
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        self.map = Map(path.join(map_folder, 'map2.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()

    def new(self):
        # Initialize all variables and do all the setup for new game.
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # =================
        # Game Loop
        # =================
        self.running = True
        while self.running:
            # Run loop at fixed speed
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Update portion of game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    # def draw_grid(self):
    #     for x in range(0, WIDTH, TILE_SIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    #     for y in range(0, HEIGHT, TILE_SIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # Catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# Create Game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
