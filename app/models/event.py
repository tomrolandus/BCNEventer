import mongoengine

from app.models.category import Category
from .base import Base
from datetime import datetime

class Event(Base):
    name = mongoengine.StringField()
    description = mongoengine.StringField()
    coordinates = mongoengine.PointField()
    address = mongoengine.StringField()
    date_time = mongoengine.DateTimeField()
    category_ids = mongoengine.ListField(mongoengine.ReferenceField(Category))

    def __init__(self, name='', description='', coordinates=(0, 0), location='', date_time=0, category_ids=None, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.description = description
        self.coordinates = coordinates
        self.location = location
        self.date_time = date_time
        self.category_ids = category_ids

        try:
            timeStamp = int(date_time) / 1000  # divide to get second from milliseconds
            self.readable_time = datetime.utcfromtimestamp(timeStamp).strftime('%a, %d %b %Y, %H:%M')
        except:
            self.readable_time = "unknown"

