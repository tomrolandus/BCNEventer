import mongoengine
from .base import Base


class Category(Base):
    name = mongoengine.StringField()

    def __init__(self, name='', *args, **values):
        super().__init__(*args, **values)
        self.name = name

    def get_id(self):
        return self.id

    def to_json(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
        }
