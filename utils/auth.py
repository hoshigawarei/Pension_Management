# utils/auth.py

from flask_login import LoginManager, login_user, logout_user, login_required
from models.user import User

login_manager = LoginManager()

def init_app(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(UserID):
    return User.query.get(int(UserID))

def login_user_account(user):
    login_user(user)

def logout_user_account():
    logout_user()
