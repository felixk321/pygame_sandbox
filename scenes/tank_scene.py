from scenes.abstract import BaseScene
from pymunk import Space, Vec2d
from components.floor import Segment
from components.tank import Tank
from pygame import Surface
import pygame
from typing import Sequence


class TankScene(BaseScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = (0,-1000)
        self.terrain = Segment((0,60), (500,60), 5, self.space)
        self.tank = Tank(Vec2d(100,190), self.space)

    def handle_pressed_keys(self, keys: Sequence[bool])-> None:
        if keys[pygame.K_a]:
            self.tank.move(-1)
        
        if keys[pygame.K_d]:
            self.tank.move(1)

    def update(self)->None:
        self.space.step(1/60)
        self.tank.rw.motor.rate *= 0.98
    
    def render(self, display: Surface)->None:
        display.fill((255,255,255))
        self.terrain.render(display)
        self.tank.render(display)

    

    
