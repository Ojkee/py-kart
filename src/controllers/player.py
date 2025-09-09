import raylib as rl
from src.controllers.controller import Controller
from src.vehicle.car import Car
from src.commands.command import *


class Player(Controller):
    def __init__(self, car: Car) -> None:
        super().__init__(car)
        self._score: int = 0

    def handle_input(self) -> list[Command]:
        commands: list[Command] = []
        if rl.IsKeyDown(rl.KEY_A):
            if rl.IsKeyDown(rl.KEY_LEFT_SHIFT):
                commands.append(SteerLeft(self._car, 1.0))
            else:
                commands.append(SteerLeft(self._car, 0.5))
        elif rl.IsKeyDown(rl.KEY_D):
            if rl.IsKeyDown(rl.KEY_LEFT_SHIFT):
                commands.append(SteerRight(self._car, 1.0))
            else:
                commands.append(SteerRight(self._car, 0.5))
        else:
            commands.append(IdleSteer(self._car))

        if rl.IsMouseButtonDown(rl.MOUSE_BUTTON_LEFT):
            commands.append(Accelerate(self._car, 0.3))
        elif rl.IsMouseButtonDown(rl.MOUSE_BUTTON_RIGHT):
            commands.append(MoveBackOrBreak(self._car, 0.2))
        else:
            commands.append(IdleMovement(self._car))
        return commands

    def update_score(self) -> None:
        self._score = self._car.checkpoints_matched

    def add_score(self, value: int) -> None:
        self._score += value

    def deactivate(self) -> None:
        return super().deactivate()
