# Inspiration:
# https://bitesofcode.wordpress.com/2020/04/09/procedural-racetrack-generation/

from __future__ import annotations
import random
import math
import numpy as np

from src.tracks.graph_structs import TrackNode, TrackEdge
from src.tracks.convex_hull import ConvexHullMethod, GrahamScan
from src.tracks.displace_methods import DisplaceMethod, DisplaceAlongNormal


class Track:
    def __init__(
        self,
        width: int,
        height: int,
        checkpoints: int,
        displace_method: DisplaceMethod | None = None,
    ) -> None:
        self._checkpoints: int = checkpoints
        self._offset_x: int = width // 8
        self._offset_y: int = height // 8
        self._displace_method: DisplaceMethod = (
            DisplaceAlongNormal() if displace_method is None else displace_method
        )

        self._center_x: int = width // 2
        self._center_y: int = height // 2

        self._nodes: list[TrackNode] = []
        self._edges: list[TrackEdge] = []
        self._inner_nodes: list[TrackNode] = []

        self._generate_nodes(width, height, checkpoints)
        self._make_convex_hull(GrahamScan())
        self._displace()
        self._insert_one_middle()

    @property
    def edges(self) -> list[TrackEdge]:
        return self._edges

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

    def _insert_one_middle(self) -> None:
        lens = list(map(lambda edge: edge.length(), self._edges))
        r_edge_idx = np.argmax(lens)
        r_edge = self._edges.pop(r_edge_idx)

        def dist_to_center(node: TrackNode) -> float:
            return math.hypot(node.x - self._center_x, node.y - self._center_y)

        dists_to_center = list(map(dist_to_center, self._inner_nodes))
        r_node_idx = np.argmin(dists_to_center)

        r_node = self._inner_nodes.pop(r_node_idx)

        self._edges.extend(
            [TrackEdge(r_edge.src, r_node), TrackEdge(r_node, r_edge.dst)]
        )

    def _displace(self) -> None:
        def mid(edge: TrackEdge) -> TrackNode:
            midx = (edge.src.x + edge.dst.x) // 2
            midy = (edge.src.y + edge.dst.y) // 2
            return TrackNode(midx, midy)

        mids = zip(list(map(mid, self._edges)), self._edges)
        displaced = list(map(self._displace_method, mids))

        value = []
        print(displaced)
        for mid_node, edge in zip(displaced, self._edges):
            value.extend([TrackEdge(edge.src, mid_node), TrackEdge(mid_node, edge.dst)])
        self._edges = value
