import pygame as pg
from pygame.transform import scale

from assets import blockSize
from collision import *
from random import randint
from functions import blit_text
from time import time
from GUI import Text


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
        self.player = CorePlayer(100, 100, "Player", scale=3, data={"Health": 10000})
        self.objects = [
            Enemy(300, 300, "Mog2129", scale=1.5, speed=3, data={"Health": 2000}),
            Object(blockSize * 3, blockSize * 4, "Crate", scale=2, data={"Health": 2000}),
        ]
        self.x_offset, self.y_offset = 0, 0
        self.healthCountText = Text(f"Health {self.player.data["Health"]}", 0, 0, (0, 0, 0), 35, "Arialblack")

    def event(self, event: pg.event.Event) -> None:
        super().event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            self.mouseDown(event)
        self.player.eventControls(event)

    def mouseDown(self, event):
        mouseX, mouseY = pg.mouse.get_pos()
        self.objects.append(
            Object(
                mouseX - (mouseX % blockSize),
                mouseY - (mouseY % blockSize),
                "Crate",
                scale=2,
                data={"Health": 2000}
            )
        )

    def tick(self) -> None:
        super().tick()

        self.player.script(self)
        collisions = self.player.collide(self.objects)
        for collision in collisions:
            if collision.type == "Enemy":
                self.player.data["Health"] -= 1
                self.healthCountText.text = f"Health {self.player.data["Health"]}"
                self.healthCountText.reload()


        # object collision
        for obj in self.objects:
            obj.script(self)
            collisions = obj.collide(self.objects)

            # enemy block breaking
            if obj.type == "Enemy":
                for collision in collisions:
                    collision.data["Health"] -= 1
                    if collision.data["Health"] < 1:
                        for obj in self.objects:
                            if id(obj) == id(collision):
                                self.objects.remove(obj)

        if randint(0, self.fps*4) == 0:
            self.objects.append(Enemy(300, 300, "Mog2129", scale=1.5, speed=3, data={"Health": 2000}))

    def display(self) -> None:
        [obj.display(self.window, self.x_offset, self.y_offset) for obj in self.objects]
        self.player.display(self.window, self.x_offset, self.y_offset)
        self.healthCountText.display(self.window)


instance = Outdoors((900, 500), "Outdoors", fps=60)
instance.start()
