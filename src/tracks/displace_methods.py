import math
import random
from abc import ABC, abstractmethod
from src.tracks.graph_structs import TrackNode, TrackEdge


class DisplaceMethod(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __call__(self, pair: tuple[TrackNode, TrackEdge]) -> TrackNode:
        pass


class DisplaceFractal(DisplaceMethod):
    def __init__(self, strength: float = 0.5) -> None:
        super().__init__()
        self._strength = strength

    def __call__(self, pair: tuple[TrackNode, TrackEdge]) -> TrackNode:
        mid, edge = pair
        max_offset = int(edge.length() * self._strength)
        dx = random.randint(-max_offset, max_offset)
        dy = random.randint(-max_offset, max_offset)
        return TrackNode(mid.x + dx, mid.y + dy)


class DisplaceGauss(DisplaceMethod):
    def __init__(self, sigma: float = 0.2) -> None:
        super().__init__()
        self._sigma = sigma

    def __call__(self, pair: tuple[TrackNode, TrackEdge]) -> TrackNode:
        mid, edge = pair
        length = edge.length()
        dx = int(random.gauss(0, self._sigma) * length)
        dy = int(random.gauss(0, self._sigma) * length)
        return TrackNode(mid.x + dx, mid.y + dy)


class DisplaceAlongNormal(DisplaceMethod):
    def __init__(self, factor: float = 0.3) -> None:
        super().__init__()
        self._factor = factor

    def __call__(self, pair: tuple[TrackNode, TrackEdge]) -> TrackNode:
        mid, edge = pair
        nx = -float(edge.dx())
        ny = float(edge.dy())
        length = math.hypot(nx, ny)
        if length == 0:
            return mid
        nx /= length
        ny /= length
        offset = self._factor * edge.length()
        dx = int(nx * offset)
        dy = int(ny * offset)
        return TrackNode(mid.x + dx, mid.y + dy)
