from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.tracks.graph_structs import TrackNode, TrackEdge


@dataclass
class ConvexHullResult:
    convex_edges: list[TrackEdge]
    inner_nodes: list[TrackNode]


class ConvexHullMethod(ABC):
    @abstractmethod
    def connect(self, nodes: list[TrackNode]) -> ConvexHullResult:
        pass

    @classmethod
    def _sign(cls, a: TrackNode, b: TrackNode, c: TrackNode) -> int:
        return (a.x - c.x) * (b.y - c.y) - (b.x - c.x) * (a.y - c.y)


class QuickHull(ConvexHullMethod):
    def __init__(self) -> None:
        super().__init__()

    def connect(self, nodes: list[TrackNode]) -> ConvexHullResult:
        import numpy as np

        xs = np.array(list(map(lambda node: node.x, nodes)))
        minx = np.min(xs)
        maxx = np.max(xs)
        # TODO
        return ConvexHullResult([], [])

    @classmethod
    def _in_triangle(
        cls, triangle: tuple[TrackNode, TrackNode, TrackNode], node: TrackNode
    ) -> bool:
        a, b, c = triangle
        signs = [
            ConvexHullMethod._sign(node, a, b),
            ConvexHullMethod._sign(node, b, c),
            ConvexHullMethod._sign(node, c, a),
        ]
        has_neg = True in [x < 0 for x in signs]
        has_pos = True in [x > 0 for x in signs]
        return not (has_neg and has_pos)


class GrahamScan(ConvexHullMethod):
    def __init__(self) -> None:
        super().__init__()

    def connect(self, nodes: list[TrackNode]) -> ConvexHullResult:
        from functools import reduce
        from itertools import pairwise

        if len(nodes) < 3:
            return ConvexHullResult([], [])

        p0 = reduce(GrahamScan._most_bottom, nodes, nodes[0])
        angle_sorted = GrahamScan._sorted_by_angle(nodes, p0)

        convex_stack: list[TrackNode] = angle_sorted[:3]
        for node in angle_sorted[3:]:
            last = convex_stack[-1]
            before = convex_stack[-2]
            while ConvexHullMethod._sign(node, last, before) < 0:
                convex_stack.pop()
                last = convex_stack[-1]
                before = convex_stack[-2]
            convex_stack.append(node)

        convex_stack.append(p0)
        convex_edges = [TrackEdge(src, dst) for src, dst in pairwise(convex_stack)]
        inner_nodes = list(filter(lambda node: not node in convex_stack, nodes))
        return ConvexHullResult(convex_edges, inner_nodes)

    @classmethod
    def _most_bottom(cls, lhs: TrackNode, rhs: TrackNode) -> TrackNode:
        if lhs.y > rhs.y:
            return lhs
        elif lhs.y == rhs.y and lhs.x > rhs.x:
            return lhs
        else:
            return rhs

    @classmethod
    def _sorted_by_angle(cls, nodes: list[TrackNode], p: TrackNode) -> list[TrackNode]:
        return sorted(nodes, key=lambda node: GrahamScan._angle(node, p), reverse=True)

    @classmethod
    def _angle(cls, a: TrackNode, b: TrackNode) -> float:
        import math

        return math.atan2(a.y - b.y, a.x - b.x)
