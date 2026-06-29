import sys
import pygame
from Configurations import Configurations

class SceneManager:
    def __init__(self, allScenes):
        self._registry = {cls.name: cls for cls in allScenes}
        self.scene = None

    def run(self, start_scene="menu"):
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        Configurations.SCREEN_W, Configurations.SCREEN_H = screen.get_size()
        pygame.display.set_caption(Configurations.TITLE)
        clock = pygame.time.Clock()
        self.switch_to(start_scene)

        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.scene.update(events)
            self.scene.draw(screen)
            pygame.display.flip()
            clock.tick(Configurations.FPS)

    def switch_to(self, sceneName):
        scene_cls = self._registry.get(sceneName)
        if scene_cls is None:
            raise ValueError(
                f"Cena '{sceneName}' não registrada. "
                f"Cenas disponíveis: {list(self._registry)}"
            )
        self.scene = scene_cls(self)