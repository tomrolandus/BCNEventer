from datetime import datetime

from flask_mongoengine import MongoEngine, Document
from mongoengine import DateTimeField

db = MongoEngine()


class Base(Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def update(self, **kwargs):
        self.updated_at = datetime.now()
        return super(Base, self).update(**kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Base, self).save(*args, **kwargs)
