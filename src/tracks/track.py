from __future__ import annotations
import random

import numpy as np
from src.tracks.graph_structs import TrackNode, TrackEdge
from src.tracks.convex_hull import ConvexHullMethod, GrahamScan


class Track:
    def __init__(self, width: int, height: int, checkpoints: int) -> None:
        self._checkpoints: int = checkpoints
        self._offset_x: int = width // 10
        self._offset_y: int = height // 10

        self._nodes: list[TrackNode] = []
        self._edges: list[TrackEdge] = []
        self._inner_nodes: list[TrackNode] = []

        self._generate_nodes(width, height, checkpoints)
        self._make_convex_hull(GrahamScan())

    def _generate_nodes(self, width: int, height: int, checkpoints: int) -> None:
        self._nodes.clear()
        for _ in range(checkpoints):
            x = random.randrange(self._offset_x, width - self._offset_x)
            y = random.randrange(self._offset_y, height - self._offset_y)
            self._nodes.append(TrackNode(x, y))

    def _make_convex_hull(self, method: ConvexHullMethod) -> None:
        result = method.connect(self._nodes)
        self._edges = result.convex_edges
        self._inner_nodes = result.inner_nodes
