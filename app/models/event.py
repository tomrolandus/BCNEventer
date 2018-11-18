from .base import Base

from datetime import datetime

class Event(Base):
    name = ""
    location = ""
    coordinates = (0, 0)
    time = ""

    def __init__(self, name, coordinates, unixTime, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.coordinates = coordinates

        try:
            timeStamp = int(unixTime)/1000 #divide to get second from milliseconds
            self.time = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            self.time = "unknown"
