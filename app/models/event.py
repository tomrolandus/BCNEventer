import mongoengine

from app.models.category import Category
from .base import Base


class Event(Base):
    name = mongoengine.StringField()
    description = mongoengine.StringField()
    location = mongoengine.PointField()
    date_time = mongoengine.DateTimeField()
    categories = mongoengine.ListField(mongoengine.ReferenceField(Category))

    def __init__(self, name='', description='', location=(0, 0), date_time=0, categories=None, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.description = description
        self.location = location
        self.date_time = date_time
        self.categories = categories

    def to_json(self, *args, **kwargs):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "date_time": self.date_time,
        }
