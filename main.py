import pygame as pg
from pygame.transform import scale

from collision import *
from random import randint
from functions import blit_text
from time import time

class Game:
    def __init__(
        self,
        resolution: tuple[int, int],
        name: str,
        fps: int = 60,
        background: tuple[int, int, int] = (255, 255, 255),
    ):
        self.width, self.height = resolution
        self.name = name
        self.window = pg.display.set_mode(resolution)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.run = True
        self.background = background
        pg.display.set_caption(name)

        self.deltaTime = 0

    def tick(self) -> None:
        self.deltaTime = self.clock.tick(self.fps) / 16
        if self.deltaTime > 1.4:
            print("[Graphics] Low FPS")


    def display(self) -> None: ...

    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.run = False
        if event.type == pg.K_F3:
            print(self.deltaTime)

    def quit(self):
        return None

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.window.fill(self.background)
            self.display()
            pg.display.update()
        return self.quit()

class Outdoors(Game):
    def __init__(
            self,
            resolution: tuple[int, int],
            name: str,
            fps: int = 60,
            background: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(resolution, name, fps, background)
        self.player = CorePlayer(100, 100, "Player", scale=3)
        self.objects = [Enemy(300, 300, "Rock", scale=3, speed=3), Object(500, 400, "Crate", scale=3)]
        self.x_offset, self.y_offset = 0, 0

    def event(self, event: pg.event.Event) -> None:
        super().event(event)
        self.player.eventControls(event)

    def tick(self) -> None:
        super().tick()
        self.player.script(self)
        self.player.collide(self.objects)
        for obj in self.objects:
            obj.script(self)
            obj.collide(self.objects)


    def display(self) -> None:
        [obj.display(self.window, self.x_offset, self.y_offset) for obj in self.objects]
        self.player.display(self.window, self.x_offset, self.y_offset)

instance = Outdoors((900, 500), "Outdoors", fps=60)
instance.start()