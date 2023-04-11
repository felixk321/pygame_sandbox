from typing import Tuple, List
import pygame
from pygame.surface import Surface
import pymunk

display = pygame.display.set_mode((500,500))
h = display.get_height()

def convert(coord : Tuple[int,int],height : int) -> Tuple[int,int]:
    return (int(coord[0]),int(height-coord[1]))

def draw_joint(display: pygame.Surface,joint: pymunk.PinJoint)->None:
    a,b = joint.anchor_a, joint.anchor_b
    world_a = joint.a.local_to_world(a)
    world_b = joint.b.local_to_world(b)
    pygame.draw.line(
        display,
        (255,255,0),
        convert(world_a, h),
        convert(world_b, h),
        5
    )