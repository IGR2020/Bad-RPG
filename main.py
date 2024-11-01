import pygame as pg
from pygame.transform import scale

from collision import CorePlayer, PushableObject, Object
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
        self.player = CorePlayer(100, 100, "Player", scale=4)
        self.objects = [PushableObject(300, 300, "Rock", 3)]
        self.void = Object(self.width-100, self.height/2, "Hole", scale=2)
        self.x_offset, self.y_offset = 0, 0
        self.money = 0
        self.startTime = time()

    def event(self, event: pg.event.Event) -> None:
        super().event(event)
        self.player.eventControls(event)

    def tick(self) -> None:
        super().tick()
        self.player.script()
        self.player.collide(self.objects)

        if randint(0, self.fps*3) == 0:
            self.objects.append(PushableObject(randint(0, self.height), randint(0, self.height), "Rock", scale=randint(2, 5)))

        for obj in self.objects:
            if pg.sprite.collide_mask(obj, self.void):
                self.objects.remove(obj)
                self.money += 1

    def display(self) -> None:
        [obj.display(self.window, self.x_offset, self.y_offset) for obj in self.objects]
        self.void.display(self.window, self.x_offset, self.y_offset)
        self.player.display(self.window, self.x_offset, self.y_offset)
        blit_text(self.window, f"Money {self.money}", (0, 0), colour=(0, 0, 0), size=30)
        blit_text(self.window, f"Time {round(time() - self.startTime)}", (0, 50), colour=(0, 0, 0), size=30)

instance = Outdoors((900, 500), "Outdoors", fps=60)
instance.start()