import raylib as rl
import math
import numpy as np

from src.contexts.context import Context
from src.rays.ray import Ray
from src.vec.vec2 import Vec2


class Collider:
    def __init__(self, track) -> None:
        self._track_image: rl.Image = rl.LoadImageFromTexture(track.texture)

    def update(self, ctx: Context) -> None:
        for car in ctx.cars:
            for ray in car.rays:
                angle_rad = math.radians(ray._angle_deg)
                origin_color = rl.GetImageColor(
                    self._track_image, int(ray.origin.x), int(ray.origin.y)
                )
                length: int = 8
                dx = math.cos(angle_rad) * length
                dy = math.sin(angle_rad) * length
                hit_x = ray.origin.x + dx
                hit_y = ray.origin.y + dy
                hit_color = rl.GetImageColor(self._track_image, int(hit_x), int(hit_y))

                while (
                    Collider.same_color(origin_color, hit_color)
                    and length <= ctx.constants.MAX_RAY_LENGTH
                ):
                    hit_color = rl.GetImageColor(
                        self._track_image,
                        int(hit_x),
                        int(hit_y),
                    )
                    length += 2
                    dx = math.cos(angle_rad) * length
                    dy = math.sin(angle_rad) * length
                    hit_x = ray.origin.x + dx
                    hit_y = ray.origin.y + dy

                ray.hit = Vec2(hit_x, hit_y)

    @classmethod
    def same_color(cls, lhs, rhs) -> bool:
        return lhs.r == rhs.r and lhs.g == rhs.g and lhs.b == lhs.b

    @classmethod
    def in_range(cls, x, y, width, height) -> bool:
        return 0 <= x and x < width and 0 <= y and y < height
