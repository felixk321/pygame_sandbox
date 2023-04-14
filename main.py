import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List, Type
from random import randint
from components.floor import Segment
from utils import convert
from components.catapult import Catapult
from scenes.abstract import BaseScene
from scenes.catapult_scene import CatapultScene

space = pymunk.Space()
space.gravity = (0,-1000)

class Game:
    def __init__(self) -> None:
        self.scene = None
        pygame.init()
        self.display = pygame.display.set_mode((500,500))
        self.scene = None
        self.clock = pygame.time.Clock()
    def run(self) ->None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.scene.handle_event(event)
            pk = pygame.key.get_pressed()
            self.scene.handle_pressed_keys(pk)

            self.scene.update()
            

            self.scene.render(self.display)

            pygame.display.update()
            self.clock.tick(60)

    def load_scene(self, Scene:Type[BaseScene])->None:
        self.scene = Scene()

g = Game()
g.load_scene(CatapultScene)
g.run()






        


