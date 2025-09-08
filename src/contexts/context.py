from dataclasses import dataclass
from src.controllers.controller import Controller
from src.tracks.track import Track
from src.vehicle.car import Car


@dataclass
class Constants:
    WINDOW_SCALE: int = 100
    WIDTH: int = WINDOW_SCALE * 16
    HEIGHT: int = WINDOW_SCALE * 9
    MAX_RAY_LENGTH: int = 96

    TRACK_WIDTH: int = 64
    CHECKPOINT_RADIUS: int = (TRACK_WIDTH - 4) // 2

    TRACK_COLOR = (211, 176, 131, 255)
    BG_COLOR = (51, 51, 51, 255)
    CHECKPOINT_COLOR = (144, 82, 82, 255)


@dataclass
class Debug:
    TRACK_NODES: bool = True


class State:
    def __init__(self, track: Track) -> None:
        self.players: list[Controller] = []
        self.track: Track = track


class Context:
    def __init__(self) -> None:
        self.constants: Constants = Constants()
        self.debug: Debug = Debug()
        self.state: State = State(self._init_track())

    def _init_track(self) -> Track:
        return Track(self.constants.WIDTH, self.constants.HEIGHT, 30)

    def add_player(self, player: Controller) -> None:
        self.state.players.append(player)

    @property
    def players(self) -> list[Controller]:
        return self.state.players

    @property
    def track(self) -> Track:
        return self.state.track

    @track.setter
    def track(self, value: Track) -> None:
        self.state.track = value

    @property
    def cars(self) -> list[Car]:
        return list(map(lambda player: player._car, self.state.players))
