from flask_script import Manager
from app.app import app
from dotenv import load_dotenv
import os

load_dotenv()

manager = Manager(app)

app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['DEBUG'] = True
if os.getenv('APP_ENV') == 'local':  # If in local mode, use debugger
    app.config['DEBUG'] = True

if __name__ == '__main__':
    manager.run()
