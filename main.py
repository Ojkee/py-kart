import raylib as rl
from src.collision.collider import Collider
from src.rays.ray import Ray
from src.contexts.context import Context
from src.vehicle.car import Car
from src.view.render import Renderer
from src.tracks.track import Track
from src.vec.vec2 import Vec2
from src.tracks.displace_methods import DisplaceFractal


def handle_input(ctx: Context) -> None:
    if rl.IsKeyDown(rl.KEY_A):
        if rl.IsKeyDown(rl.KEY_LEFT_SHIFT):
            ctx.cars[0].steer_left(1)
        else:
            ctx.cars[0].steer_left(0.5)
    elif rl.IsKeyDown(rl.KEY_D):
        if rl.IsKeyDown(rl.KEY_LEFT_SHIFT):
            ctx.cars[0].steer_right(1)
        else:
            ctx.cars[0].steer_right(0.5)
    else:
        ctx.cars[0].center_steering()

    if rl.IsMouseButtonDown(rl.MOUSE_BUTTON_LEFT):
        ctx.cars[0].accelerate(0.3)
    elif rl.IsMouseButtonDown(rl.MOUSE_BUTTON_RIGHT):
        ctx.cars[0].accelerate(-0.2)
    else:
        ctx.cars[0].slow_down()


def update(ctx: Context) -> None:
    ctx.cars[0].update()


def main() -> None:
    ctx = Context()
    renderer = Renderer(ctx.constants.WIDTH, ctx.constants.HEIGHT)

    start_node = ctx.track.starting_node()
    start_angle = ctx.track.starting_angle_degree()
    ctx.add_car(car=Car(start_node.x, start_node.y, start_angle, 8))

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
