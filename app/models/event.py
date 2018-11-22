import mongoengine

from app.models.category import Category
from .base import Base


class Event(Base):
    name = mongoengine.StringField()
    description = mongoengine.StringField()
    location = mongoengine.PointField()
    date_time = mongoengine.DateTimeField()
    category_ids = mongoengine.ListField(mongoengine.ReferenceField(Category))

    def __init__(self, name='', description='', location=(0, 0), date_time=0, category_ids=None, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.description = description
        self.location = location
        self.date_time = date_time
        self.category_ids = category_ids
