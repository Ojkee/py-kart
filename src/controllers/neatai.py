import math
import numpy as np
from neat import nn

from src.controllers.controller import Controller
from src.vehicle.car import Car
from src.commands.command import *
from src.vec.vec2 import Vec2


class NeatAI(Controller):
    def __init__(self, car: Car, genome, net: nn.FeedForwardNetwork) -> None:
        super().__init__(car)
        self.genome = genome
        self.net: nn.FeedForwardNetwork = net
        self._steering_commands: list[Command] = [
            SteerLeft(self._car, 0.5),
            # SteerLeft(self._car, 1.0),
            # SteerRight(self._car, 1.0),
            IdleSteer(self._car),
            SteerRight(self._car, 0.5),
        ]
        self._movement_commands: list[Command] = [
            MoveBackOrBreak(self._car, 0.2),
            IdleMovement(self._car),
            Accelerate(self._car, 0.3),
        ]

    def handle_input(self) -> list[Command]:
        d = self._next_checkpoint_delta()
        velocity = (
            self._car._velocity / self._car.MAX_SPEED_FORWARD
            if self._car._velocity < 0
            else self._car._velocity / self._car.MAX_SPEED_BACKWARD
        )
        # TODO: refacotor, 96 is max ray len
        input = tuple(abs(ray) / 96 for ray in self._car.rays) + (
            velocity,
            self._car._steering_angle() / 45,
            d.x / 100,
            d.y / 100,
        )
        output = np.array(self.net.activate(input))

        # Outputs are in range (-1,1)
        steer_idx = round((output[0] + 1) / 2 * (len(self._steering_commands) - 1))
        movement_idx = round((output[1] + 1) / 2 * (len(self._movement_commands) - 1))

        return [
            self._steering_commands[steer_idx],
            self._movement_commands[movement_idx],
        ]

    def update_score(self) -> None:
        self.genome.fitness = self._car.checkpoints_matched * 10
        d = self._next_checkpoint_delta()
        dist = math.hypot(d.x, d.y) / 100
        self.genome.fitness -= dist

    def add_score(self, value: int) -> None:
        self.genome.fitness += value

    def deactivate(self) -> None:
        return super().deactivate()

    def _next_checkpoint_delta(self) -> Vec2:
        if not self._car.next_checkpoint:
            return Vec2(0, 0)
        dx = self._car.next_checkpoint.x - self._car._pos.x
        dy = self._car.next_checkpoint.y - self._car._pos.y
        return Vec2(dx, dy)

    @staticmethod
    def softmax(nums: np.ndarray) -> np.ndarray:
        return np.exp(nums) / np.sum(np.exp(nums), axis=0)
