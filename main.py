import raylib as rl
import os
import neat

from src.controllers.player import Player
from src.controllers.neatai import NeatAI
from src.collision.collider import Collider
from src.contexts.context import Context
from src.vehicle.car import Car
from src.view.render import Renderer


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
            player_car = Car(start_node.x, start_node.y, start_angle)
            player = Player(player_car)
            self.ctx.add_player(player)

        rl.InitWindow(ctx.constants.WIDTH, ctx.constants.HEIGHT, b"Py-kart")
        rl.SetTargetFPS(self.ctx.constants.TARGET_FPS)

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

    def _update(self, *, should_remove: bool = False) -> None:
        self.collider.update(self.ctx)
        for i, player in enumerate(reversed(self.ctx.players)):
            if player._car.active:
                player._car.update()
            elif should_remove:
                self.ctx.players.pop(i)

        for player in self.ctx.players:
            player.update_score()

    def eval_genomes(self, genomes, config):
        self.ctx.players.clear()
        start_node = self.ctx.track.starting_node()
        start_angle = self.ctx.track.starting_angle_degree()
        for _, genome in genomes:
            genome.fitness = 0.0
            neat_car = Car(start_node.x, start_node.y, start_angle, 8)
            neat_net = neat.nn.FeedForwardNetwork.create(genome, config)
            neat_controller = NeatAI(neat_car, genome, neat_net)
            self.ctx.add_player(neat_controller)

        MAX_TICKS = self.ctx.constants.LEARN_TIME_SEC * self.ctx.constants.TARGET_FPS

        tick: int = 0
        while not rl.WindowShouldClose():
            self._handle_input()
            self._update(should_remove=False)
            self.renderer.draw(self.ctx)
            if not any(self.ctx.cars):
                break

            tick += 1
            if tick >= MAX_TICKS:
                break


if __name__ == "__main__":
    game = Game(playable=False, num_ai=0)

    local_dir = os.path.dirname(__file__)
    neat_config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        os.path.join(local_dir, "cfg", "neat-config.txt"),
    )
    population = neat.Population(neat_config)
    population.run(game.eval_genomes, 50)
