import raylib as rl
from src.contexts.context import Context
from src.vehicle.car import Car
from src.view.render import Renderer
from src.tracks.track import Track
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

    if rl.IsMouseButtonDown(rl.MOUSE_BUTTON_LEFT):
        ctx.cars[0].accelerate(0.5)
    elif rl.IsMouseButtonDown(rl.MOUSE_BUTTON_RIGHT):
        ctx.cars[0].accelerate(-0.3)
    else:
        ctx.cars[0].slow_down()


def update(ctx: Context) -> None:
    ctx.cars[0].update()


def main() -> None:
    ctx = Context()
    renderer = Renderer(ctx.constants.WIDTH, ctx.constants.HEIGHT)
    ctx.track = Track(
        ctx.constants.WIDTH, ctx.constants.HEIGHT, 100, DisplaceFractal(0.2)
    )
    # ctx.add_car(car=Car(400, 300, 0))

    rl.InitWindow(ctx.constants.WIDTH, ctx.constants.HEIGHT, b"Py-kart")
    rl.SetTargetFPS(60)

    renderer.bake_track(ctx.track)

    while not rl.WindowShouldClose():
        # handle_input(ctx)
        # update(ctx)
        renderer.draw(ctx.cars)


if __name__ == "__main__":
    main()
