from flask import Flask, Blueprint, render_template, request, jsonify, url_for, flash
from models.user import User
from models.eldercareinstitution import ElderCareInstitution
from models.staffinstitution import StaffInstitution  # 导入StaffInstitution
from models.userrole import UserRole  # 导入UserRoles
from models.reservation import Reservation
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required
from extensions import db
from sqlalchemy.sql import func
from datetime import datetime


def get_user_role(user_id):
    user_role = UserRole.query.filter_by(UserID=user_id).first()
    if user_role:
        return user_role.Role
    return None

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservation', methods=['GET'])
@login_required
def reservation_page():
    # 获取所有养老院和殡葬机构
    elder_care_institutions = ElderCareInstitution.query.all()

    return render_template('reservation_page.html', institutions=elder_care_institutions)

@reservation_bp.route('/book', methods=['POST'])
@login_required
def book_reservation():
    role = get_user_role(current_user.UserID)
    
    # 判断用户是否为“老年用户”或“家属、看护用户”
    if role not in ['老年用户', '家属、看护用户']:
        return jsonify({"status": "error", "message": "您没有权限进行预约"}), 403

    # 获取预约数据
    institution_id = request.json.get('institution_id')
    reservation_time = request.json.get('reservation_time')
    
    if not reservation_time:
        return jsonify({"status": "error", "message": "预约时间不能为空"}), 400

    # 将预约时间转换为 datetime 对象
    reservation_time = datetime.strptime(reservation_time, "%Y-%m-%dT%H:%M")
    max_id = db.session.query(func.max(Reservation.ReservationID)).scalar()
    next_id = max_id + 1 if max_id is not None else 400001

    # 创建预约记录
    reservation = Reservation(
        ReservationID=next_id,
        UserID=current_user.UserID,
        InstitutionID=institution_id,
        Role=role,
        ReservationTime=reservation_time,
        ReservationStatus=1  # 默认状态为待确认
    )
    
    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "预约成功",
        "reservation_id": reservation.ReservationID
    })

@reservation_bp.route('/my_reservations', methods=['GET'])
@login_required
def my_reservations():
    # 查询当前用户的所有预约信息
    reservations = Reservation.query.filter_by(UserID=current_user.UserID).all()
    
    # 状态映射
    status_mapping = {
        1: "待机构确认",
        2: "预约成功",
        3: "预约已逾期",
        4: "服务已完成"
    }
    
    # 构建返回数据
    reservation_list = []
    for reservation in reservations:
        institution = ElderCareInstitution.query.filter_by(InstitutionID=reservation.InstitutionID).first()
        reservation_list.append({
            "reservation_id": reservation.ReservationID,
            "institution_name": institution.InstitutionName if institution else "未知机构",
            "reservation_time": reservation.ReservationTime.strftime("%Y-%m-%d %H:%M"),
            "status": status_mapping.get(reservation.ReservationStatus, "未知状态")
        })
    
    return jsonify({
        "status": "success",
        "reservations": reservation_list
    })

