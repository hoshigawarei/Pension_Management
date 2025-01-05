# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# 创建扩展实例
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)  # 初始化 login_manager
    login_manager.login_view = "user.login"  # 登录视图（即登录页面的路由名）
    bcrypt.init_app(app)


