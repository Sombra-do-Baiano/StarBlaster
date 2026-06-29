import pygame
import sys

from Configurations import Configurations
from Scenes.BaseScene import Scene
from UI.Button import Button
from UI.Text import Text
from UI.Colors import BLACK, WHITE, DIM

def CreateSave(typeOfPet):
    return

class MainGameScene(Scene):
    name = "maingame"

    def __init__(self, manager):
        super().__init__(manager)
        self.font_title = pygame.font.SysFont(None, 96)
        self.font_sub = pygame.font.SysFont(None, 30)

        center_w = Configurations.SCREEN_W // 2
        center_y = Configurations.SCREEN_H // 2

        self.btn_dog = Button("Cachorro", center_w, 35 + center_y)
        self.btn_cat = Button("Gato", center_w, 110 + center_y)
        self.title = Text

    def handle_event(self, event):
        if self.btn_dog.handle_event(event):
            CreateSave("Cachorro")
            self.manager.switch_to("game")
        if self.btn_cat.handle_event(event):
            CreateSave("Gato")
            self.manager.switch_to("game")
        if self.btn_quit.handle_event(event):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def draw(self, surface):
        surface.fill(BLACK)
        
        self.btn_new.draw(surface)
        self.btn_load.draw(surface)
        self.btn_quit.draw(surface)