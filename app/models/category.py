import mongoengine
from .base import Base


class Category(Base):
    name = mongoengine.StringField()

    def __init__(self, name='', *args, **values):
        super().__init__(*args, **values)
        self.name = name
