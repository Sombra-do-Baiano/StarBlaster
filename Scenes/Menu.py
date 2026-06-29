import pygame
import sys

from Configurations import Configurations
from Scenes.BaseScene import Scene
from UI.Button import Button
from UI.Text import Text
from UI.Colors import BLACK, WHITE, DIM


class MenuScene(Scene):
    name = "menu"

    def __init__(self, manager):
        super().__init__(manager)

        self.font_title = pygame.font.SysFont(None, 96)
        self.font_sub = pygame.font.SysFont(None, 30)

        center_w = Configurations.SCREEN_W // 2
        center_y = Configurations.SCREEN_H // 2

        self.btn_new = Button("Novo Jogo", center_w, 50 + center_y, 36, 350, 75, WHITE, True)
        self.btn_load = Button("Carregar Jogo", center_w, 150 + center_y, 36, 350, 75, WHITE, True)
        self.btn_quit = Button("Sair", center_w, 250 + center_y, 36, 350, 75, WHITE, True)

        self.text_title = Text(
            Configurations.TITLE,
            Configurations.SCREEN_W // 2,
            -110 + Configurations.SCREEN_H // 2,
            WHITE,
            36,
            True
        )

        self.text_esc_to_quit = Text(
            "Pressione Esc para sair",
            Configurations.SCREEN_W // 2,
            350 + Configurations.SCREEN_H // 2,
            DIM,
            36,
            True
        )

        self.scene = pygame.sprite.Group()
        self.scene.add(
            self.btn_new,
            self.btn_load,
            self.btn_quit,
            self.text_title,
            self.text_esc_to_quit
        )

    def handle_event(self, event):
        if self.btn_new.handle_event(event):
            self.manager.switch_to("newgame")

        if self.btn_load.handle_event(event):
            self.manager.switch_to("maingame")

        if self.btn_quit.handle_event(event):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def update(self, events):
        for event in events:
            self.handle_event(event)

    def draw(self, surface):
        surface.fill(BLACK)

        pygame.draw.line(
            surface,
            DIM,
            (Configurations.SCREEN_W / 20, -35 + Configurations.SCREEN_H // 2),
            (Configurations.SCREEN_W * 19 / 20, -35 + Configurations.SCREEN_H // 2),
            1,
        )

        self.scene.draw(surface)