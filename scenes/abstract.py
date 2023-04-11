from pygame.event import Event
from pygame.surface import Surface
from typing import Sequence

class BaseScene:
    def __init__(self) -> None:
        pass

    def handle_event(self, event:Event) ->None:
        pass
    def handle_pressed_keys(self, keys: Sequence[bool]) -> None:
        pass
    def update(self)->None:
        pass
    def render(self, display:Surface) ->None:
        pass
class CatapultScene(BaseScene):
    def __init__(self) -> None:
        pass
    