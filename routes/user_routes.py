from flask import Blueprint, render_template, request, jsonify,  url_for,flash, redirect
from models.user import User,SeniorUser, FamilyCareGiver, Staff, Supervisor, FamilySeniorRelation
from models.userrole import UserRole 
from models.eldercareinstitution import ElderCareInstitution 
from models.funeralinstitution import FuneralInstitution
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required
from extensions import db
from werkzeug.security import generate_password_hash


user_bp = Blueprint('user', __name__)

bcrypt = Bcrypt()

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(Username=username).first()

        if user:
            # 如果密码是明文的，重新哈希并更新数据库
            if not user.Password.startswith('$2b$'):
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user.Password = hashed_password
                db.session.commit()

            # 检查哈希密码
            if bcrypt.check_password_hash(user.Password, password):
                login_user(user)
                return jsonify({"status": "success", "redirect_url": "/user/dashboard"})
        
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return render_template('login.html')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    user_role = UserRole.query.filter_by(UserID=user.UserID).first()  # 获取用户角色

    # 返回用户信息和角色
    return render_template('dashboard.html', user=user, role=user_role.Role)

@user_bp.route('/view_institutions', methods=['GET', 'POST'])
@login_required
def view_institutions():
    search_term = request.args.get('search', '')  # 获取搜索关键词
    street_town_filter = request.args.get('street_town', '')  # 获取StreetTown的筛选条件
    page = request.args.get('page', 1, type=int)
    institutions = []
    street_towns = []  # 用来存储所有唯一的 StreetTown 值

    table_type = request.args.get('type', '')  # 获取机构类型，'elderly' 或 'funeral'

    search_feedback = None
    if table_type == 'elderly':
        # 查找养老机构
        query = ElderCareInstitution.query.filter(ElderCareInstitution.InstitutionName.like(f'%{search_term}%'))
        
        # 如果有StreetTown的筛选条件，应用它
        if street_town_filter:
            query = query.filter(ElderCareInstitution.StreetTown == street_town_filter)
        
        institutions = query.paginate(page=page, per_page=10, error_out=False)
        # 获取所有唯一的 StreetTown 值，作为下拉框的选项
        street_towns = db.session.query(ElderCareInstitution.StreetTown).distinct().all()

    elif table_type == 'funeral':
        # 查找殡葬机构
        query = FuneralInstitution.query.filter(FuneralInstitution.InstitutionName.like(f'%{search_term}%'))
        
        # 如果搜索term为空，不做过滤
        if search_term:
            if not search_term:
                institutions = []
            else:
                query = query.filter(FuneralInstitution.Address.like(f'%{search_term}%'))

        if street_town_filter:
            query = query.filter(FuneralInstitution.Address == street_town_filter)
        
        institutions = query.paginate(page=page, per_page=10, error_out=False)
        # 获取所有唯一的 StreetTown 值，作为下拉框的选项
        street_towns = db.session.query(FuneralInstitution.Address).distinct().all()

    # 获取上一个页面的 URL
    referrer = request.referrer

    return render_template('view_institutions.html', 
                           institutions=institutions, 
                           table_type=table_type,
                           search_term=search_term,
                           street_towns=street_towns,
                           street_town_filter=street_town_filter,
                           search_feedback='No results found' if not institutions else None,
                           referrer=referrer)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # 提供注册页面

    # 获取注册信息
    username = request.form.get('username')
    password = request.form.get('password')
    phone_number = request.form.get('phone_number')
    user_type = request.form.get('user_type')
    real_name = request.form.get('real_name')
    id_number = request.form.get('id_number')
    residence = request.form.get('residence')
    position = request.form.get('position')
    employee_number = request.form.get('employee_number')
    senior_user_id = request.form.get('senior_user_id')

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(Username=username).first()
    if existing_user:
        flash('用户名已存在，请选择其他用户名。')
        return redirect(url_for('user.register'))  # 返回注册页面

    # 获取当前最大 UserID，并设置新用户的 UserID
    max_user_id = db.session.query(db.func.max(User.UserID)).scalar() or 0
    new_user_id = max_user_id + 1

    try:
        # 添加到 `users` 表
        new_user = User(
            UserID=new_user_id,
            Username=username,
            Password=generate_password_hash(password),
            PhoneNumber=phone_number
        )
        db.session.add(new_user)
        db.session.commit()

        # 添加到 `UserRole` 表
        role_id = int(user_type)  # 1-5
        role_name = {1: '一般用户', 2: '老年用户', 3: '家属、看护用户', 4: '机构管理用户', 5: '民政部门用户'}[role_id]
        new_user_role = UserRole(
            UserID=new_user_id,
            RoleID=role_id,
            Role=role_name
        )
        db.session.add(new_user_role)
        db.session.commit()

        # 根据用户类型添加到对应表
        if role_id == 2:  # 老年用户
            senior_user = SeniorUser(
                UserID=new_user_id,
                RealName=real_name,
                IDNumber=id_number,
                Residence=residence
            )
            db.session.add(senior_user)

        elif role_id == 3:  # 家属/看护用户
            senior_user = SeniorUser.query.filter_by(UserID=senior_user_id).first()
            if not senior_user:
                flash('绑定的老年用户不存在，请检查输入的老年用户ID')
                return redirect(url_for('user.register'))

            family_caregiver = FamilyCareGiver(
                UserID=new_user_id,
                RealName=real_name,
                IDNumber=id_number
            )
            db.session.add(family_caregiver)
            db.session.commit()

            # 更新 `familyseniorrelation` 表
            family_relation = FamilySeniorRelation(
                FamilyCaregiverID=new_user_id,
                SeniorUserID=senior_user_id
            )
            db.session.add(family_relation)

        elif role_id == 4:  # 机构管理用户
            staff = Staff(
                UserID=new_user_id,
                Position=position
            )
            db.session.add(staff)

        elif role_id == 5:  # 民政部门用户
            supervisor = Supervisor(
                UserID=new_user_id,
                Position=position,
                EmployeeNumber=employee_number
            )
            db.session.add(supervisor)

        # 提交所有更改
        db.session.commit()

        flash('注册成功！')
        return redirect(url_for('user.login'))  # 注册成功后跳转到登录页面

    except Exception as e:
        db.session.rollback()  # 回滚数据库操作
        flash(f'注册失败，请重试。错误: {str(e)}')
        return redirect(url_for('user.register'))  # 注册失败返回注册页面

