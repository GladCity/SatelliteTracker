from typing import Tuple
import datetime


class Satellite:
    def __init__(self, id: int, name: str, start_pos: Tuple[float, float], start_time: datetime, period: float,
                 height: float,
                 photo_bounds: Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float]],
                 detalis: float, photo_size: float):
        self.id = id
        self.name = name
        self.start_pos = start_pos
        self.start_time = start_time
        self.period = period
        self.height = height
        self.photo_bounds = photo_bounds
        self.detalis = detalis
        self.photo_size = photo_size

    def __str__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.start_pos) + " " + str(self.start_time) + " " + str(
            self.period) + " " + str(self.height) + " " + str(self.photo_bounds) + " " + str(self.detalis) + " " + str(
            self.photo_size)
