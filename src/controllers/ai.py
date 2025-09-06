from src.controllers.controller import Controller
from src.vehicle.car import Car
from src.commands.command import *


class AI(Controller):
    def __init__(self, car: Car) -> None:
        super().__init__(car)

    def handle_input(self) -> list[Command]:
        # TODO: Implement
        return []
