from .base import Base


class Event(Base):
    name = ""
    location = ""
    coordinates = (0, 0)

    def __init__(self, name, coordinates, time, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.coordinates = coordinates
        self.time = time
