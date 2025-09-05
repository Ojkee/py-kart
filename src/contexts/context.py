from dataclasses import dataclass
from src.vehicle.car import Car
from src.tracks.track import Track


@dataclass
class Constants:
    WINDOW_SCALE: int = 100
    WIDTH: int = WINDOW_SCALE * 16
    HEIGHT: int = WINDOW_SCALE * 9
    MAX_RAY_LENGTH: int = 96


class State:
    def __init__(self, track: Track) -> None:
        self.cars: list[Car] = []
        self.track: Track = track


class Context:
    def __init__(self) -> None:
        self.constants: Constants = Constants()
        self.state: State = State(self._init_track())

    def _init_track(self) -> Track:
        return Track(self.constants.WIDTH, self.constants.HEIGHT, 100)

    def add_car(self, car: Car) -> None:
        self.state.cars.append(car)

    @property
    def cars(self) -> list[Car]:
        return self.state.cars

    @property
    def track(self) -> Track:
        return self.state.track

    @track.setter
    def track(self, value: Track) -> None:
        self.state.track = value
