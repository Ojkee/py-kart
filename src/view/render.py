import raylib as rl
from src.vehicle.car import Car
from src.tracks.track import Track


class Renderer:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._track_texture: rl.RenderTexture | None = None

    def bake_track(self, track: Track) -> None:
        nodes = track._edges_to_sorted_nodes()
        nodes_as_tuple = list(map(lambda node: (node.x, node.y), nodes))
        closed = nodes_as_tuple[-2:] + nodes_as_tuple + nodes_as_tuple[:2]
        track_texture = rl.LoadRenderTexture(self._width, self._height)

        rl.BeginTextureMode(track_texture)
        rl.ClearBackground([51, 51, 51, 255])
        rl.DrawSplineCatmullRom(closed, len(closed), 64, rl.BEIGE)
        rl.EndTextureMode()
        self._track_texture = track_texture

    def draw(self, cars: list[Car]) -> None:
        rl.BeginDrawing()
        rl.ClearBackground([51, 51, 51, 255])
        rl.DrawFPS(4, 4)

        self._draw_track()
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

    def _draw_track(self) -> None:
        if self._track_texture:
            rl.DrawTexture(self._track_texture.texture, 0, 0, rl.WHITE)
