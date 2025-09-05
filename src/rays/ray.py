from src.vec.vec2 import Vec2


class Ray:
    def __init__(self, x: int, y: int, angle_deg: float) -> None:
        self._origin: Vec2 = Vec2(x, y)
        self._angle_deg: float = angle_deg
        self._angle_deg_relative: float = angle_deg
        self._length: float = 0

        self._hit: Vec2 | None = None

    @property
    def origin(self) -> Vec2:
        return self._origin

    @origin.setter
    def origin(self, value: Vec2) -> None:
        self._origin = value

    @property
    def hit(self) -> Vec2 | None:
        return self._hit

    @hit.setter
    def hit(self, value: Vec2) -> None:
        self._hit = value

    @property
    def angle_deg_relative(self) -> float:
        return self._angle_deg_relative

    @angle_deg_relative.setter
    def angle_deg_relative(self, value: float) -> None:
        self._angle_deg_relative = value

    @property
    def angle_deg(self) -> float:
        return self._angle_deg

    @angle_deg.setter
    def angle_deg(self, value: float) -> None:
        self._angle_deg = value

    def __repr__(self) -> str:
        return f"{self.origin} -> {self.hit}\n"
