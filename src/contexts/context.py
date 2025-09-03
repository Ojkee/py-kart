from src.tracks.track import Track
from src.vehicle.car import Car


class Context:
    def __init__(self) -> None:
        self._cars: list[Car] = []
        self._track: Track | None = None

    def add_car(self, car: Car) -> None:
        self._cars.append(car)

    @property
    def cars(self) -> list[Car]:
        return self._cars

    @property
    def track(self) -> Track | None:
        return self._track
