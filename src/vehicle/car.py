from __future__ import annotations
import math
import random
from enum import Enum
from dataclasses import dataclass
import numpy as np


from src.rays.ray import Ray
from src.vec.vec2 import Vec2
from .constants import SCALE


class Car:
    WIDTH: int = 12 * SCALE
    HEIGHT: int = 25 * SCALE
    OFFSET_Y: int = HEIGHT // 5

    MAX_SPEED_FORWARD: float = 4 * SCALE
    MAX_SPEED_BACKWARD: float = 2 * SCALE

    # CENTRE OF rotation_degree
    MAX_COR_Y = 10 * SCALE
    COR_DIST_X: float = 25 * SCALE

    DISTANCE_FRONT_BACK_WHEELS: int = HEIGHT - 2 * OFFSET_Y
    EPS = 10e-1
    MIN_STEER_TILT = 1

    def __init__(
        self,
        start_x: float,
        start_y: float,
        starting_rotation_degree: float = 0,
        num_rays: int = 0,
    ) -> None:
        self._pos: Vec2 = Vec2(start_x, start_y)

        self._rotation_degree: float = starting_rotation_degree
        self._velocity: float = 0.0

        self._cor_y: float = 0

        self._wheels = self._init_wheels()
        self._rays: list[Ray] = self._init_rays(num_rays)

        self._color: list[int] = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            255,
        ]

        self.active: bool = True

        self.checkpoints_matched: int = 1
        self._next_checkpoint: Vec2 | None = None

        self.update()

    def _init_wheels(self) -> dict[WheelPos, Wheel]:
        w2 = self.WIDTH / 2
        h2 = self.HEIGHT / 2
        wheels = {
            WheelPos.LEFT_FRONT: Wheel(self, -w2, -h2 + self.OFFSET_Y),
            WheelPos.RIGHT_FRONT: Wheel(self, w2, -h2 + self.OFFSET_Y),
            WheelPos.LEFT_BACK: Wheel(self, -w2, h2 - self.OFFSET_Y),
            WheelPos.RIGHT_BACK: Wheel(self, w2, h2 - self.OFFSET_Y),
        }
        return wheels

    def _init_rays(self, num_rays: int) -> list[Ray]:
        if num_rays <= 0:
            return []

        angle = 360 / num_rays
        rays: list[Ray] = []
        for i in range(0, num_rays):
            ray = Ray(int(self._pos.x), int(self._pos.y), i * angle)
            rays.append(ray)
        return rays

    def __bool__(self) -> bool:
        return self.active

    @property
    def rays(self) -> list[Ray]:
        return self._rays

    @property
    def rotation_degree(self) -> float:
        return self._rotation_degree

    @rotation_degree.setter
    def rotation_degree(self, value: float) -> None:
        self._rotation_degree = value

    @property
    def rect(self) -> tuple[int, int, int, int]:
        x = int(self._pos.x + self.WIDTH / 2)
        y = int(self._pos.y + self.HEIGHT / 2)
        return (
            x,
            y,
            self.WIDTH,
            self.HEIGHT,
        )

    @property
    def color(self) -> list[int]:
        return self._color

    @property
    def next_checkpoint(self) -> Vec2 | None:
        return self._next_checkpoint

    @next_checkpoint.setter
    def next_checkpoint(self, value: Vec2) -> None:
        self._next_checkpoint = value

    def accelerate(self, force: float) -> None:
        v = self._velocity + force
        v = max(-self.MAX_SPEED_BACKWARD, v)
        self._velocity = min(self.MAX_SPEED_FORWARD, v)

    def move(self) -> None:
        self._move_forward()
        if self._cor_pos_relative() == None:
            return
        delta_rad = math.radians(self._steering_angle())
        self._rotation_degree += math.degrees(
            self._velocity / self.DISTANCE_FRONT_BACK_WHEELS * math.tan(delta_rad)
        )

    def _move_forward(self):
        self._pos.add(self._delta_pos())

    def _delta_pos(self) -> np.ndarray:
        angle_rad = math.radians(self._rotation_degree)
        unit_direction = np.array([math.sin(angle_rad), -math.cos(angle_rad)])
        return unit_direction * self._velocity

    def update(self) -> None:
        self.move()
        for pos, wheel in self._wheels.items():
            new_pos = (
                np.dot(self._rotation_matrix(), wheel._car_relative_pos.content)
                + self._pos.content
            )
            self._wheels[pos].move(new_pos[0], new_pos[1])
        self._update_wheels_tilt()
        self._update_rays()

    def slow_down(self) -> None:
        if abs(self._velocity) < self.EPS:
            self._velocity = 0
        else:
            self._velocity *= 0.99

    def wheels_pos(self) -> list[WheelInfo]:
        value: list[WheelInfo] = []
        for _, wheel in self._wheels.items():
            value.append(
                WheelInfo(
                    int(wheel.pos.x),
                    int(wheel.pos.y),
                    wheel.WIDTH,
                    wheel.HEIGHT,
                    wheel.rotation_degree,
                )
            )
        return value

    def steer_left(self, force: float) -> None:
        self._cor_y = max(self._cor_y - force * SCALE, -self.MAX_COR_Y)

    def steer_right(self, force: float) -> None:
        self._cor_y = min(self._cor_y + force * SCALE, self.MAX_COR_Y)

    def center_steering(self) -> None:
        self._cor_y *= 0.9

    def rotate(self, angle_degree: float) -> None:
        self._rotation_degree += angle_degree
        if self._rotation_degree < 0:
            self._rotation_degree += 360
        elif self._rotation_degree >= 360:
            self._rotation_degree -= 360

    def cor_pos(self) -> Vec2 | None:
        pos = self._cor_pos_relative()
        if pos == None:
            return None
        pos.content += self._pos.content
        return pos

    def _cor_pos_relative(self) -> Vec2 | None:
        if abs(self._cor_y) < self.MIN_STEER_TILT:
            return None
        local_x = -self.COR_DIST_X if self._cor_y < 0 else self.COR_DIST_X
        local_y = abs(self._cor_y) - self.HEIGHT / 2 + self.OFFSET_Y
        local = Vec2(local_x, local_y)
        local.rotate(self._rotation_matrix())
        return local

    def _steering_angle(self) -> float:
        lhs = self._wheels[WheelPos.LEFT_FRONT].tilt
        rhs = self._wheels[WheelPos.RIGHT_FRONT].tilt
        return (lhs + rhs) / 2.0

    def _update_wheels_tilt(self) -> None:
        cor = self.cor_pos()
        self._update_wheel_tilt(cor, WheelPos.LEFT_FRONT)
        self._update_wheel_tilt(cor, WheelPos.RIGHT_FRONT)

    def _update_wheel_tilt(self, cor: Vec2 | None, pos: WheelPos) -> None:
        if cor == None:
            self._wheels[pos].tilt = 0
            return
        angle = self._angle_between(cor, self._wheels[pos].pos)
        angle_degrees = math.degrees(angle)
        angle_raw = angle_degrees - self._rotation_degree
        self._wheels[pos].tilt = self._norm(angle_raw)

    def _norm(self, angle: float) -> float:
        angle = (angle + 180) % 360 - 180
        return angle

    def _angle_between(self, a: Vec2, b: Vec2) -> float:
        if self._cor_y > 0:
            return math.atan2(b.y - a.y, b.x - a.x) - math.pi
        else:
            return math.atan2(a.y - b.y, a.x - b.x) + math.pi

    def _rotation_matrix(self) -> np.ndarray:
        angle = math.radians(self._rotation_degree)
        sin = math.sin(angle)
        cos = math.cos(angle)
        return np.array([[cos, -sin], [sin, cos]])

    def _update_rays(self) -> None:
        for ray in self._rays:
            ray.angle_deg = ray.angle_deg_relative + self.rotation_degree
            ray.origin = self._pos


class Wheel:
    WIDTH: int = 4 * SCALE
    HEIGHT: int = 8 * SCALE

    def __init__(self, parent: Car, x: float, y: float) -> None:
        self._parent: Car = parent
        self._car_relative_pos: Vec2 = Vec2(x, y)

        self._pos: Vec2 = Vec2(0, 0)
        self._tilt: float = 0.0

    @property
    def rotation_degree(self) -> float:
        return self._parent.rotation_degree + self._tilt

    @property
    def tilt(self) -> float:
        return self._tilt

    @tilt.setter
    def tilt(self, value: float) -> None:
        self._tilt = value

    @property
    def pos(self) -> Vec2:
        return self._pos

    def move(self, x: float, y: float) -> None:
        self._pos = Vec2(x, y)


@dataclass
class WheelInfo:
    x: int
    y: int
    width: int
    height: int
    angle: float


class WheelPos(Enum):
    LEFT_FRONT = 1
    RIGHT_FRONT = 2
    LEFT_BACK = 3
    RIGHT_BACK = 4
