import numpy as np
from neat import nn

from src.controllers.controller import Controller
from src.vehicle.car import Car
from src.commands.command import *


class NeatAI(Controller):
    def __init__(self, car: Car, genome, net: nn.FeedForwardNetwork) -> None:
        super().__init__(car)
        self.genome = genome
        self.net: nn.FeedForwardNetwork = net
        self._steering_commands: list[Command] = [
            SteerLeft(self._car, 0.5),
            SteerLeft(self._car, 1.0),
            SteerRight(self._car, 0.5),
            SteerRight(self._car, 1.0),
            IdleSteer(self._car),
        ]
        self._movement_commands: list[Command] = [
            Accelerate(self._car, 0.3),
            MoveBackOrBreak(self._car, 0.2),
            IdleMovement(self._car),
        ]

    def handle_input(self) -> list[Command]:
        input = tuple(abs(ray) for ray in self._car.rays) + (
            self._car._velocity,
            self._car._steering_angle(),
        )
        output = np.array(self.net.activate(input))

        steering = NeatAI.softmax(output[3:])
        steer_idx = np.argmax(steering)

        movement = NeatAI.softmax(output[:3])
        movement_idx = np.argmax(movement)

        return [
            self._steering_commands[steer_idx],
            self._movement_commands[movement_idx],
        ]

    def update_score(self) -> None:
        self.genome.fitness = self._car.checkpoints_matched

    def add_score(self, value: int) -> None:
        self.genome.fitness += value

    @staticmethod
    def softmax(nums: np.ndarray) -> np.ndarray:
        return np.exp(nums) / np.sum(np.exp(nums), axis=0)
