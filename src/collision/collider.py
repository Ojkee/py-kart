import raylib as rl

import math

from src.contexts.context import Context
from src.rays.ray import Ray
from src.vec.vec2 import Vec2

from functools import cache


class Collider:
    def __init__(self, track_texture) -> None:
        self._track_colors: list[rl.Color] = self._init_track_colors(track_texture)
        self._track_width: int = track_texture.width

    def _init_track_colors(self, track_texture):
        track_image = rl.LoadImageFromTexture(track_texture)
        return rl.LoadImageColors(track_image)

    def update(self, ctx: Context) -> None:
        track_color = Collider.track_rl_color(ctx.constants.TRACK_COLOR)

        for car in ctx.cars:
            if not car.active:
                continue

            current_color = self._color_at(car._pos.x, car._pos.y)
            if not Collider.same_color(current_color, track_color):
                car.active = False
                continue
            self._update_car_rays(ctx, car.rays)

    def _update_car_rays(self, ctx: Context, rays: list[Ray]) -> None:
        for ray in rays:
            angle_rad = math.radians(ray.angle_deg)
            origin_color = self._color_at(ray.origin.x, ray.origin.y)
            length: int = 8
            hit = Collider.ray_point(ray.origin, angle_rad, length)

            def should_grow() -> bool:
                return (
                    Collider.in_range(
                        hit.x, hit.y, ctx.constants.WIDTH, ctx.constants.HEIGHT
                    )
                    and Collider.same_color(origin_color, self._color_at(hit.x, hit.y))
                    and length <= ctx.constants.MAX_RAY_LENGTH
                )

            while should_grow():
                length += 2
                hit = Collider.ray_point(ray.origin, angle_rad, length)
            ray.hit = hit

    @classmethod
    @cache
    def track_rl_color(cls, color: tuple[int, int, int, int]):
        return rl.ffi.new("struct Color *", color)

    def _color_at(self, x: float, y: float):
        return self._track_colors[int(y) * self._track_width + int(x)]

    @classmethod
    def delta(cls, angle: float, length: float) -> tuple[float, float]:
        dx = math.cos(angle) * length
        dy = math.sin(angle) * length
        return dx, dy

    @classmethod
    def ray_point(cls, origin: Vec2, angle_rad: float, length: float) -> Vec2:
        dx, dy = Collider.delta(angle_rad, length)
        return origin.added(dx, dy)

    @classmethod
    def same_color(cls, lhs, rhs) -> bool:
        return lhs.r == rhs.r and lhs.g == rhs.g and lhs.b == rhs.b

    @classmethod
    def in_range(cls, x, y, width, height) -> bool:
        return 0 <= x and x < width and 0 <= y and y < height
