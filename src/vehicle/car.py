from __future__ import annotations
import math
import random
from enum import Enum
from dataclasses import dataclass


from .constants import SCALE


class Wheel:
    WIDTH: int = 4 * SCALE
    HEIGHT: int = 8 * SCALE

    def __init__(self, parent: Car, x: float, y: float) -> None:
        self._parent: Car = parent
        self.pos_x: float = x
        self.pos_y: float = y

        self.x: float = 0
        self.y: float = 0
        self._tilt: float = 0.0

    @property
    def width(self) -> int:
        return self.WIDTH

    @property
    def height(self) -> int:
        return self.HEIGHT

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
    def pos(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


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


class Car:
    WIDTH: int = 12 * SCALE
    HEIGHT: int = 25 * SCALE
    OFFSET_Y: int = 6 * SCALE

    MAX_SPEED_FORWARD: float = 4 * SCALE
    MAX_SPEED_BACKWARD: float = 2 * SCALE

    # CENTRE OF rotation_degree
    MAX_COR_Y = 10 * SCALE
    COR_DIST_X: float = 25 * SCALE

    DISTANCE_FRONT_BACK_WHEELS: int = HEIGHT - 2 * OFFSET_Y
    EPS = 10e-1
    MIN_STEER_TILT = 1

    def __init__(
        self, start_x: float, start_y: float, starting_rotation_degree: float = 0
    ) -> None:
        self._x: float = start_x
        self._y: float = start_y

        self._rotation_degree: float = starting_rotation_degree
        self._velocity: float = 0.0

        self._cor_y: float = 0

        self._wheels = self.init_wheels()

        self._color: list[int] = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            255,
        ]

        self.update()

    def init_wheels(self) -> dict[WheelPos, Wheel]:
        w2 = self.WIDTH / 2
        h2 = self.HEIGHT / 2
        wheels = {
            WheelPos.LEFT_FRONT: Wheel(self, -w2, -h2 + self.OFFSET_Y),
            WheelPos.RIGHT_FRONT: Wheel(self, w2, -h2 + self.OFFSET_Y),
            WheelPos.LEFT_BACK: Wheel(self, -w2, h2 - self.OFFSET_Y),
            WheelPos.RIGHT_BACK: Wheel(self, w2, h2 - self.OFFSET_Y),
        }
        return wheels

    @property
    def rotation_degree(self) -> float:
        return self._rotation_degree

    @rotation_degree.setter
    def rotation_degree(self, value: float) -> None:
        self._rotation_degree = value

    @property
    def rect(self) -> tuple[int, int, int, int]:
        return (
            int(self._x + self.WIDTH / 2),
            int(self._y + self.HEIGHT / 2),
            self.WIDTH,
            self.HEIGHT,
        )

    @property
    def color(self) -> list[int]:
        return self._color

    def accelerate(self, force: float) -> None:
        v = self._velocity + force
        v = max(-self.MAX_SPEED_BACKWARD, v)
        self._velocity = min(self.MAX_SPEED_FORWARD, v)

    def move(self) -> None:
        cor = self._cor_pos_relative()
        if cor == None:
            self._move_forward()
            return
        delta_rad = math.radians(self._steering_angle())
        phi_rad = math.radians(self._rotation_degree)
        self._x += self._velocity * math.sin(phi_rad)
        self._y -= self._velocity * math.cos(phi_rad)
        self._rotation_degree += math.degrees(
            self._velocity / self.DISTANCE_FRONT_BACK_WHEELS * math.tan(delta_rad)
        )

    def _move_forward(self):
        dx = math.sin(math.radians(self._rotation_degree)) * self._velocity
        dy = math.cos(math.radians(self._rotation_degree)) * self._velocity
        self._x += dx
        self._y += -dy

    def update(self) -> None:
        rot_radians = math.radians(self.rotation_degree)
        sin_angle = math.sin(rot_radians)
        cos_angle = math.cos(rot_radians)
        self.move()
        for pos, wheel in self._wheels.items():
            x: int = int(self._x + wheel.pos_x * cos_angle - wheel.pos_y * sin_angle)
            y: int = int(self._y + wheel.pos_x * sin_angle + wheel.pos_y * cos_angle)
            self._wheels[pos].move(x, y)
        self._update_wheels_tilt()

    def slow_down(self) -> None:
        if abs(self._velocity) < self.EPS:
            self._velocity = 0
        else:
            self._velocity *= 0.99

    def wheels_pos(self) -> list[WheelInfo]:
        value: list[WheelInfo] = []
        for _, wheel in self._wheels.items():
            x: int = int(wheel.x)
            y: int = int(wheel.y)
            value.append(
                WheelInfo(x, y, wheel.WIDTH, wheel.HEIGHT, wheel.rotation_degree)
            )
        return value

    def steer_left(self, force: float) -> None:
        self._cor_y = max(self._cor_y - force * SCALE, -self.MAX_COR_Y)

    def steer_right(self, force: float) -> None:
        self._cor_y = min(self._cor_y + force * SCALE, self.MAX_COR_Y)

    def rotate(self, angle_degree: float) -> None:
        self._rotation_degree += angle_degree
        if self._rotation_degree < 0:
            self._rotation_degree += 360
        elif self._rotation_degree >= 360:
            self._rotation_degree -= 360

    def cor_pos(self) -> tuple[float, float] | None:
        pos = self._cor_pos_relative()
        if pos == None:
            return None
        x, y = pos
        return x + self._x, y + self._y

    def _cor_pos_relative(self) -> tuple[float, float] | None:
        if abs(self._cor_y) < self.MIN_STEER_TILT:
            return None
        local_x = -self.COR_DIST_X if self._cor_y < 0 else self.COR_DIST_X
        local_y = abs(self._cor_y) - self.HEIGHT / 2 + self.OFFSET_Y
        sin_angle = math.sin(math.radians(self._rotation_degree))
        cos_angle = math.cos(math.radians(self._rotation_degree))
        x = local_x * cos_angle - local_y * sin_angle
        y = local_x * sin_angle + local_y * cos_angle
        return x, y

    def _steering_angle(self) -> float:
        lhs = self._wheels[WheelPos.LEFT_FRONT].tilt
        rhs = self._wheels[WheelPos.RIGHT_FRONT].tilt
        return (lhs + rhs) / 2.0

    def _update_wheels_tilt(self) -> None:
        cor = self.cor_pos()
        self._update_wheel_tilt(cor, WheelPos.LEFT_FRONT)
        self._update_wheel_tilt(cor, WheelPos.RIGHT_FRONT)

    def _update_wheel_tilt(
        self, cor: tuple[float, float] | None, pos: WheelPos
    ) -> None:
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

    def _angle_between(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        if self._cor_y > 0:
            return math.atan2(b[1] - a[1], b[0] - a[0]) - math.pi
        else:
            return math.atan2(a[1] - b[1], a[0] - b[0]) + math.pi
