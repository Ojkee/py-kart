import numpy as np


class Vec2:
    def __init__(self, x: float, y: float) -> None:
        self.content = np.array([x, y], dtype=np.float32)

    @property
    def x(self) -> float:
        return self.content[0]

    @x.setter
    def x(self, value: float) -> None:
        self.content[0] = value

    @property
    def y(self) -> float:
        return self.content[1]

    @y.setter
    def y(self, value: float) -> None:
        self.content[1] = value

    def __repr__(self) -> str:
        return f"{int(self.x)}, {int(self.y)}"

    def rotate(self, matrix: np.ndarray) -> None:
        self.content = np.dot(matrix, self.content)

    def rotated(self, matrix: np.ndarray) -> np.ndarray:
        return np.dot(matrix, self.content)

    def add(self, vec: np.ndarray) -> None:
        self.content += vec

    def added(self, vec: np.ndarray) -> np.ndarray:
        return self.content + vec
