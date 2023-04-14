from scenes.abstract import BaseScene
from components.catapult import Catapult
from components.floor import Segment
from pymunk import Space
from pygame.surface import Surface
from pygame.event import Event
import pygame
from typing import Sequence

class CatapultScene(BaseScene):
    def __init__(self) -> None:
        self.space = Space()
        self.catapult = Catapult(250, 300, 75, self.space)
        self.floor = Segment((0,60),(500,60), 5,self.space)
        self.space.gravity = (0,-1000)

        self.bullets = []

    def update(self) -> None:
        self.space.step(1/60)
        ammo = self.catapult.detach_ammo()
        if ammo:
            self.bullets.append(ammo)



    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                self.catapult.reload()
            if event.key == pygame.K_SPACE:
                self.catapult.shot()
    def handle_pressed_keys(self, keys: Sequence[bool]) -> None:
        if keys[pygame.K_LEFT]:
            self.catapult.move_arm()
        if keys[pygame.K_d]:
            self.catapult.move(-1)
        if keys[pygame.K_a]:
            self.catapult.move(1)

       
    def render(self, display: Surface) ->None:
        display.fill((255,255,255))
        self.catapult.render(display)
        self.floor.render(display)
        for b in self.bullets:
            b.render(display)
