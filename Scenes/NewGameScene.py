import pygame
import sys

from Configurations import Configurations
from Scenes.BaseScene import Scene
from UI.Button import Button
from UI.Text import Text
from UI.Colors import BLACK, WHITE, DIM

def CreateSave(typeOfPet):
    return

class NewGameScene(Scene):
    name = "newgame"

    def __init__(self, manager):
        super().__init__(manager)
        self.font_title = pygame.font.SysFont(None, 96)
        self.font_sub = pygame.font.SysFont(None, 30)

        center_w = Configurations.SCREEN_W // 2
        center_y = Configurations.SCREEN_H // 2

        self.text_choose = Text('Escolha seu PET!',center_w, center_y - 160)
        self.warning = Text('AO ESCOLHER SEU PET ANTERIOR SERÁ APAGADO',center_w, center_y - 80)
        self.btn_dog = Button("Cachorro", center_w - 200, center_y, 36, 300, 60, WHITE, True)
        self.btn_cat = Button("Gato", center_w + 200, center_y, 36, 300, 60, WHITE, True)
        self.btn_back = Button("Voltar", center_w, center_y + 160, 36, 300, 60, WHITE, True)

        self.scene = pygame.sprite.Group()
        self.scene.add(self.text_choose, self.warning, self.btn_dog)

    def handle_event(self, event):
        if self.btn_dog.handle_event(event):
            CreateSave("Cachorro")
            self.btn_dog.turn_invisible()
            self.btn_cat.turn_invisible()
            #self.manager.switch_to("maingame")
        if self.btn_cat.handle_event(event):
            CreateSave("Gato")
            self.btn_dog.turn_invisible()
            self.btn_cat.turn_invisible()
            #self.manager.switch_to("maingame")
        if self.btn_back.handle_event(event):
            self.manager.switch_to("menu")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def draw(self, surface):
        surface.fill(BLACK)
        
        self.scene.draw(surface)