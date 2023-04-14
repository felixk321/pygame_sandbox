import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List
from random import randint
from components.floor import Segment
from utils import convert
from components.catapult import Catapult
pygame.init()

display = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
h = display.get_height()

bullets = []

space = pymunk.Space()
space.gravity = (0,-1000)





catapult = Catapult(250,300,75,space)

line = Segment((0,100),(500,100),5,space)




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:

            self.scene.update()
            

            self.scene.render(self.display)

            pygame.display.update()
            self.clock.tick(60)

    def load_scene(self, Scene:Type[BaseScene])->None:
        self.scene = Scene()

g = Game()
g.load_scene(CatapultScene)
g.run()






        


