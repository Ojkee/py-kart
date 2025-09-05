import raylib as rl

# import numpy as np
import math

from functools import cache

from src.contexts.context import Context
from src.rays.ray import Ray
from src.vec.vec2 import Vec2


class Collider:
    def __init__(self, track) -> None:
        self._track_image: rl.Image = rl.LoadImageFromTexture(track.texture)

    def update(self, ctx: Context) -> None:
        for car in ctx.cars:
            self._update_car_rays(ctx, car.rays)

    def _update_car_rays(self, ctx: Context, rays: list[Ray]) -> None:
        for ray in rays:
            angle_rad = math.radians(ray._angle_deg)
            origin_color = self._color_at(ray.origin.x, ray.origin.y)
            length: int = 8
            dx, dy = Collider.delta(angle_rad, length)
            hit = ray.origin.added(dx, dy)

            def shoud_grow() -> bool:
                return (
                    Collider.same_color(origin_color, self._color_at(hit.x, hit.y))
                    and length <= ctx.constants.MAX_RAY_LENGTH
                )

            while shoud_grow():
                length += 2
                dx, dy = Collider.delta(angle_rad, length)
                hit = ray.origin.added(dx, dy)
            ray.hit = hit

    def _color_at(self, x: float, y: float):
        return rl.GetImageColor(self._track_image, int(x), int(y))

    @classmethod
    @cache
    def delta(cls, angle: float, length: float) -> tuple[float, float]:
        dx = math.cos(angle) * length
        dy = math.sin(angle) * length
        return dx, dy

    @classmethod
    def same_color(cls, lhs, rhs) -> bool:
        return lhs.r == rhs.r and lhs.g == rhs.g and lhs.b == lhs.b

    @classmethod
    def in_range(cls, x, y, width, height) -> bool:
        return 0 <= x and x < width and 0 <= y and y < height
