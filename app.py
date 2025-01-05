# app.py

from flask import Flask, render_template
from extensions import db, login_manager
from utils.auth import init_app as init_auth  # 导入init_app
from flask_migrate import Migrate
from routes.user_routes import user_bp
from routes.review_routes import review_bp
from routes.review_routes import report_bp
from routes.healthdata_routes import heartrate_bp
from routes.emergency_routes import emergencycall_bp
from routes.reservation_routes import reservation_bp
from routes.institution_routes import institution_bp
from routes.report_routes import manage_report_bp
from config import Config
from models.user import User

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)

# 初始化扩展
db.init_app(app)
migrate = Migrate(app, db)

# 初始化登录管理器
init_auth(app)  # 调用utils/auth.py中的init_app函数来初始化login_manager

# 设置登录管理器的视图
login_manager.login_view = 'user.login'

# 设置用户加载器
@login_manager.user_loader
def load_user(UserID):
    return User.query.get(int(UserID))


# 注册路由蓝图
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(review_bp, url_prefix='/review')
app.register_blueprint(report_bp, url_prefix='/review')
app.register_blueprint(heartrate_bp, url_prefix='/healthdata')
app.register_blueprint(emergencycall_bp, url_prefix='/emergency')
app.register_blueprint(reservation_bp, url_prefix='/reservation')
app.register_blueprint(institution_bp, url_prefix='/institution')
app.register_blueprint(manage_report_bp, url_prefix='/manage_report')

# 为根路径添加路由
@app.route('/')
def home():
    return render_template('index.html')

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
