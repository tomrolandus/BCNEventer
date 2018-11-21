import mongoengine
from .base import Base


class Event(Base):
    name = mongoengine.StringField()
    description = mongoengine.StringField()
    coordinates = mongoengine.PointField()
    time = mongoengine.DateTimeField()

    def __init__(self, name, coordinates, unix_time, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.coordinates = coordinates
        self.time = unix_time
