import mongoengine
from .base import Base


class Category(Base):
    name = mongoengine.StringField()

    def __init__(self, name='', *args, **values):
        super().__init__(*args, **values)
        self.name = name

    def as_json(self):
        obj = {
            'id': str(self.id),
            'name': str(self.name),
        }

        return obj

    def to_json(self):
        obj = {
            'id': str(self.id),
            'name': str(self.name),
        }

        return obj

    def get_id(self):
        return self.id