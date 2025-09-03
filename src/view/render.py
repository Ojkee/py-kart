import raylib as rl
from src.vehicle.car import Car
from src.tracks.track import Track


class Renderer:
    def __init__(self) -> None:
        pass

    def draw(self, track: Track, cars: list[Car]) -> None:
        rl.BeginDrawing()
        rl.DrawFPS(4, 4)

        rl.ClearBackground([51, 51, 51, 255])
        for car in cars:
            self._draw_car(car)

        rl.EndDrawing()

    def _draw_car(self, car: Car) -> None:
        x, y, w, h = car.rect
        w2 = w / 2
        h2 = h / 2
        for wheel in car.wheels_pos():
            rl.DrawRectanglePro(
                (wheel.x, wheel.y, wheel.width, wheel.height),
                [wheel.width / 2, wheel.height / 2],
                wheel.angle,
                rl.BLACK,
            )
        rl.DrawRectanglePro(
            (x - w2, y - h2, w, h), [w2, h2], car.rotation_degree, car.color
        )
