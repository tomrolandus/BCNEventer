from flask_pymongo import PyMongo
from flask import Flask, render_template
import csv
from .event import Event
import os
from .settings import APP_ROOT

app = Flask(__name__)

app.config.from_pyfile('../settings.cfg', silent=False)

mongo = PyMongo(app)

@app.route('/')
def index():
    events = getEvents()
    return render_template('index.html', events = events)

def getEvents():
    events = []
    with open(os.path.join(APP_ROOT, 'static/events_Barcelona.csv'), 'rt') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            new_event = Event(row[3],(row[0],row[1]),row[2])
            events.append(new_event)
    return events

