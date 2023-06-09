from pygame import Surface, Rect
from pygame.math import Vector2
from pygame.image import load
from typing import Optional

class Animation:
    def __init__(self, filename: str, frames: int, frame_size: Vector2) -> None:
        self.tile = load(filename)
        self.frames = frames
        self.frame_size = frame_size
        self.running = False #checks if animation should be rendered
        self.active_frame = 20
        self.pos: Optional[Vector2] = None

    def get_coords(self, frame_n: int)->Vector2:

        cols_n = self.tile.get_width() // self.frame_size.x
        rows_n = self.tile.get_height() // self.frame_size.y

        x = (frame_n % cols_n)* self.frame_size.x
        y = (frame_n // rows_n)* self.frame_size.y

        return Vector2(x, y)
    
    def start(self, pos: Vector2)-> None:
         self.pos = pos
         self.running = True
         self.active_frame = 0
         
    def update(self)->None:
        if self.active_frame == self.frames -1 :
             self.running = False
             self.active_frame = 0
             self.pos = None
             return
        self.active_frame += 1
        

    def render(self, display: Surface, shift_x: int)->None:
        if not self.running or self.pos is None:
            return
        coords = self.get_coords(self.active_frame)
        rect = Rect(coords, self.frame_size)
        tile = self.tile.subsurface(rect)
        display.blit(tile, self.pos - Vector2(shift_x, 0))


class ExplosionAnimation(Animation):
        pass