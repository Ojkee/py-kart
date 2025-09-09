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

    @abstractmethod
    def update_score(self) -> None:
        pass

    @abstractmethod
    def add_score(self, value: int) -> None:
        pass

    @abstractmethod
    def deactivate(self) -> None:
        self._car.active = False
