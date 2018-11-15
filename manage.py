import os
from dotenv import load_dotenv
from flask_script import Manager
from app.app import app

load_dotenv()

manager = Manager(app)

if os.getenv('APP_ENV') == 'local':  # If in local mode, use debugger
    app.config['DEBUG'] = True

if __name__ == '__main__':
    manager.run()
