from flask_script import Manager
from app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
