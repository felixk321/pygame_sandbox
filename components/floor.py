import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List
from random import randint
from utils import convert

class Segment:
    def __init__(self, startCoord: Tuple[int, int], endCoord: Tuple[int,int], thickness: int, s: pymunk.Space) -> None:
        self.startCoord = startCoord
        self.endCoord=endCoord
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, startCoord, endCoord, thickness)
        self.shape.elasticity = 1
        self.shape.friction = 1
        s.add(self.body,self.shape)

    def render(self, display :pygame.Surface):
        h = display.get_height()
        pygame.draw.line(display, (255,0,0),convert(self.startCoord,h),convert(self.endCoord,h),5)
