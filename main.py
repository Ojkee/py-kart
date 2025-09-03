import raylib as rl
from src.contexts.context import Context
from src.vehicle.car import Car
from src.view.render import Renderer
from src.tracks.track import Track


def main() -> None:
    renderer = Renderer()
    ctx = Context()
    ctx.add_car(car=Car(400, 300, 0))

    rl.InitWindow(800, 600, "Py-kart".encode())
    rl.SetTargetFPS(60)

    while not rl.WindowShouldClose():
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

        ctx.cars[0].update()
        renderer.draw(Track(), ctx.cars)


if __name__ == "__main__":
    main()
