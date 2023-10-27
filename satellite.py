class Satellite:
    def __init__(self, id: int, name: str, tle: str, detalis: float, photo_size: float):
        self.id = id
        self.name = name
        self.tle = tle
        self.detalis = detalis
        self.photo_size = photo_size

    def __str__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.tle) + " " + str(self.detalis) + " " + str(
            self.photo_size)
