class Event(object):
    name = ""
    location = ""
    coordinates = (0,0)

    def __init__(self, name, coordinates, time):
        self.name = name
        self.coordinates = coordinates
        self.time = time