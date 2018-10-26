from flask_script import Manager
from app.app import App

manager = Manager(App)

# TODO: make this an environment variable
# Dont forget to comment this out in production
App.config['DEBUG'] = True

if __name__ == '__main__':
    manager.run()
