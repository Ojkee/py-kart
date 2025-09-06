from abc import ABC, abstractmethod

from src.vehicle.car import Car


class Command(ABC):
    def __init__(self, car: Car) -> None:
        self._car: Car = car

    @abstractmethod
    def execute(self) -> None:
        pass


class IdleMovement(Command):
    def __init__(self, car: Car) -> None:
        super().__init__(car)

    def execute(self) -> None:
        self._car.slow_down()


class Accelerate(Command):
    def __init__(self, car: Car, force: float) -> None:
        super().__init__(car)
        self._force: float = force

    def execute(self) -> None:
        self._car.accelerate(self._force)


class MoveBackOrBreak(Command):
    def __init__(self, car: Car, force: float) -> None:
        super().__init__(car)
        self._force: float = force

    def execute(self) -> None:
        self._car.accelerate(-self._force)


class IdleSteer(Command):
    def __init__(self, car: Car) -> None:
        super().__init__(car)

    def execute(self) -> None:
        self._car.center_steering()


class SteerLeft(Command):
    def __init__(self, car: Car, force: float) -> None:
        super().__init__(car)
        self._force: float = force

    def execute(self) -> None:
        self._car.steer_left(self._force)


class SteerRight(Command):
    def __init__(self, car: Car, force: float) -> None:
        super().__init__(car)
        self._force: float = force

    def execute(self) -> None:
        self._car.steer_right(self._force)
