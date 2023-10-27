class Satellite:
    def __init__(self, id: int, name: str, norad_id: int, details: float, photo_size: float):
        self.id = id
        self.name = name
        self.norad_id = norad_id
        self.details = details
        self.photo_size = photo_size

    def __str__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.tle) + " " + str(self.details) + " " + str(
            self.photo_size)
