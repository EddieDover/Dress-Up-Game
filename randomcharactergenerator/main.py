import io
from random import randint
import pygame as pg

# from pygame import mixer
from os.path import join
import os
from os import walk
from sys import exit

# import tkinter
import ctypes
import pywinauto

import pyautogui

# from random import randint

import settings


class Player(pg.sprite.Sprite):
    def __init__(self, groups, parts):
        super().__init__(groups)
        self.parts = parts
        self.skin_colors = ["fair", "pale_brown"]
        self.races = ["human", "cat"]
        self.hairstyles = ["emo"]
        self.hair_colors = ["black", "blonde", "brown"]
        self.bottoms = ["shorts", "skirt"]
        self.chests = ["cropped_shirt", "bra"]
        self.tops = ["none", "jacket", "coat", 'cropped_hoodie']
        self.socks = ["none", "leggings", "thigh_highs"]
        self.change_appearance()
        self.rect = self.image.get_frect(topleft=(settings.W * .5, 0))

    def change_appearance(self):
        surf = pg.Surface((1766, 2513), pg.SRCALPHA)

        skin_colors_idx = randint(0, len(self.skin_colors) - 1)
        hairstyles_idx = randint(0, len(self.hairstyles) - 1)
        hair_colors_idx = randint(0, len(self.hair_colors) - 1)
        races_idx = randint(0, len(self.races) - 1)
        tops_idx = randint(0, len(self.tops) - 1)
        bottoms_idx = randint(0, len(self.bottoms) - 1)
        socks_idx = randint(0, len(self.socks) - 1)
        chests_idx = randint(0, len(self.chests) - 1)

        if self.tops[tops_idx] != 'none': 
            surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'top_{self.tops[tops_idx]}_back1.png')).convert_alpha())
        if self.races[races_idx] == "cat":
            surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'tail_cat_{self.hair_colors[hair_colors_idx]}.png')).convert_alpha())
        if self.tops[tops_idx] != 'none': 
            surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'top_{self.tops[tops_idx]}_back2.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'hair_{self.hairstyles[hairstyles_idx]}_{self.hair_colors[hair_colors_idx]}_back.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'body_{self.skin_colors[skin_colors_idx]}.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'socks_{self.socks[socks_idx]}.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'bottom_{self.bottoms[bottoms_idx]}.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'chest_{self.chests[chests_idx]}.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'arm_{self.skin_colors[skin_colors_idx]}.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'top_{self.tops[tops_idx]}_front.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'face_purple.png')).convert_alpha())
        if self.races[races_idx] == "cat":
            surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'catear_back_{self.hair_colors[hair_colors_idx]}.png')).convert_alpha())
        else: 
            surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'humanear_{self.skin_colors[skin_colors_idx]}.png')).convert_alpha())
        surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'hair_{self.hairstyles[hairstyles_idx]}_{self.hair_colors[hair_colors_idx]}_front.png')).convert_alpha())
        if self.races[races_idx] == "cat":
            surf.blit(pg.image.load(join('assets', 'img', 'player_pieces', f'catear_front_{self.hair_colors[hair_colors_idx]}.png')).convert_alpha())

        data = pg.image.tobytes(surf, "RGBA")
        final_surf = pg.image.frombytes(data, (1766, 2513), "RGBA")
        final_surf = pg.transform.scale_by(final_surf, .4)
        self.image = final_surf


class Game:

    def __init__(self):

        # Setup
        pg.init()
        pg.font.init()
        ctypes.windll.user32.SetProcessDPIAware()  # keeps Windows GUI scale settings from messing with resolution
        monitor_size = pg.display.list_modes()[0]
        self.display = pg.display.set_mode((settings.W, settings.H))
        self.fullscreen = False
        pg.display.set_caption("Dress Up Game")
        if not self.fullscreen:  # These just slow down game launch if done in fullscreen
            os.environ["SDL_VIDEO_CENTERED"] = "1"  # Centers window
            # app = pywinauto.Application().connect(title_re="Dress Up Game")
            # app.top_window().set_focus() # Activates window
        self.clock = pg.time.Clock()
        self.running = True

        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_location = os.path.join(current_dir, "assets")

        # Imports
        self.player_parts = {
            "legs": [],
            "cat_tails": [],
            "emo_hair_backs": [],
            "torsos": [],
            "bottoms": [],
            "tops": [],
            "human_heads": [],
            "cat_heads": [],
            "cat_ears": [],
            "faces": [],
            "emo_hair_fronts": [],
        }
        for part in self.player_parts.keys():
            for folder_path, sub_folders, file_names in walk(join(asset_location, "img", "parts", part)):
                if file_names:
                    for file_name in file_names:
                        path = join(folder_path, file_name)
                        surf = pg.image.load(path).convert_alpha()
                        self.player_parts[part].append(surf)

        # Sprites
        self.sprites = pg.sprite.Group()
        self.player = Player(self.sprites, self.player_parts)

    def run(self):

        # Loop
        while self.running:
            self.dt = self.clock.tick() / 1000
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    if event.key == pg.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.display = pg.display.set_mode((settings.W, settings.H), pg.FULLSCREEN)
                        else:
                            self.display = pg.display.set_mode((settings.W, settings.H))
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.player.change_appearance()
            # Render
            self.display.blit(pg.image.load(join('assets', 'img', 'test_bg.png')).convert_alpha())
            self.sprites.draw(self.display)
            pg.display.flip()

        pg.quit()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
