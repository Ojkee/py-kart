from dataclasses import dataclass
import math


@dataclass(frozen=True)
class TrackNode:
    x: int
    y: int

    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y


@dataclass(frozen=True)
class TrackEdge:
    src: TrackNode
    dst: TrackNode

    def length(self) -> float:
        dx = self.src.x - self.dst.x
        dy = self.src.y - self.dst.y
        return math.hypot(dx, dy)

    def dx(self) -> int:
        return self.dst.x - self.src.x

    def dy(self) -> int:
        return self.dst.y - self.src.y
