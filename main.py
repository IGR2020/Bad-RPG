import pygame as pg
from collision import CorePlayer

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

    def tick(self) -> None:
        self.clock.tick(self.fps)

    def display(self) -> None: ...

    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.run = False

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

    def event(self, event: pg.event.Event) -> None:
        super().event(event)
        self.player.eventControls(event)

    def tick(self) -> None:
        super().tick()
        self.player.script()
        self.player.collide([])

    def display(self) -> None:
        self.player.display(self.window)

instance = Outdoors((900, 500), "Outdoors")
instance.start()