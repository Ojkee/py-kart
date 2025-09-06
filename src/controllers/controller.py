import raylib as rl
from abc import ABC, abstractmethod

from src.commands.command import *
from src.vehicle.car import Car


class Controller(ABC):
    def __init__(self, car: Car) -> None:
        super().__init__()
        self._car: Car = car

    def __repr__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def handle_input(self) -> list[Command]:
        pass


class Player(Controller):
    def __init__(self, car: Car) -> None:
        super().__init__(car)

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


class AI(Controller):
    def __init__(self, car: Car) -> None:
        super().__init__(car)

    def handle_input(self) -> list[Command]:
        # TODO: Implement
        return []
