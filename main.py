import raylib as rl
from src.controllers.controller import Player
from src.collision.collider import Collider
from src.contexts.context import Context
from src.vehicle.car import Car
from src.view.render import Renderer


def handle_input(ctx: Context) -> None:
    for player in ctx.players:
        for command in player.handle_input():
            command.execute()


def update(ctx: Context) -> None:
    for car in ctx.cars:
        car.update()
        car.move()


def main() -> None:
    ctx = Context()
    renderer = Renderer(ctx.constants.WIDTH, ctx.constants.HEIGHT)

    start_node = ctx.track.starting_node()
    start_angle = ctx.track.starting_angle_degree()
    ctx.add_player(Player(Car(start_node.x, start_node.y, start_angle, 8)))

    rl.InitWindow(ctx.constants.WIDTH, ctx.constants.HEIGHT, b"Py-kart")
    rl.SetTargetFPS(60)

    renderer.bake_track(ctx.track)

    collider = Collider(renderer._track_texture.texture)

    while not rl.WindowShouldClose():
        handle_input(ctx)
        update(ctx)
        collider.update(ctx)
        renderer.draw(ctx)


if __name__ == "__main__":
    main()
