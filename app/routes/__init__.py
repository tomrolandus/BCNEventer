from flask_login import LoginManager

from app.models.user import User
from .web import web

login_manager = LoginManager()
login_manager.login_view = 'web.login'


@login_manager.user_loader
def load_user(user_id):
    if user_id == 'None':
        return None

    return User.objects(pk=user_id).first()


def init_app(app):
    login_manager.init_app(app)
    app.register_blueprint(web)
