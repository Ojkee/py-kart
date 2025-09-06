import raylib as rl

from src.controllers.player import Player
from src.controllers.ai import AI
from src.collision.collider import Collider
from src.contexts.context import Context
from src.vehicle.car import Car
from src.view.render import Renderer
from src.vec.vec2 import Vec2


class Game:
    def __init__(self, *, playable: bool = False, num_ai: int = 0) -> None:
        self._playable = playable
        self._num_ai = num_ai
        self.ctx = Context()
        self.renderer = Renderer(self.ctx.constants.WIDTH, self.ctx.constants.HEIGHT)
        self.collider: Collider

        self._init(self.ctx, self.renderer)

    def _init(self, ctx: Context, renderer: Renderer) -> None:
        start_node = self.ctx.track.starting_node()
        start_angle = self.ctx.track.starting_angle_degree()

        if self._playable:
            self.ctx.add_player(Player(Car(start_node.x, start_node.y, start_angle)))

        for _ in range(self._num_ai):
            ai_car = Car(start_node.x, start_node.y, start_angle, 7)
            ai = AI(ai_car)
            self.ctx.add_player(ai)

        rl.InitWindow(ctx.constants.WIDTH, ctx.constants.HEIGHT, b"Py-kart")
        rl.SetTargetFPS(60)

        renderer.bake_track(ctx)

        self.collider = Collider(renderer._track_texture.texture)

    def run(self) -> None:
        while not rl.WindowShouldClose():
            self._handle_input()
            self._update()
            self.renderer.draw(self.ctx)

    def _handle_input(self) -> None:
        for player in self.ctx.players:
            for command in player.handle_input():
                command.execute()

    def _update(self) -> None:
        self.collider.update(self.ctx)
        for car in self.ctx.cars:
            if car.active:
                car.update()


if __name__ == "__main__":
    game = Game(playable=True, num_ai=0)
    game.run()
