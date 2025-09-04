from dataclasses import dataclass


@dataclass
class TrackNode:
    x: int
    y: int


@dataclass
class TrackEdge:
    src: TrackNode
    dst: TrackNode
