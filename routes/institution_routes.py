from flask import Blueprint, render_template, request, jsonify, url_for
from models.user import User
from models.userrole import UserRole
from models.eldercareinstitution import ElderCareInstitution
from models.funeralinstitution import FuneralInstitution
from models.staffinstitution import StaffInstitution
from models.reservation import Reservation
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required
from extensions import db
from sqlalchemy.orm import aliased

institution_bp = Blueprint('institution', __name__)

@institution_bp.route('/manage_institution')
@login_required
def manage_institution():
    # 获取当前用户 ID
    user_id = current_user.UserID

    # 定义两个别名，分别表示养老机构和殡葬机构
    elder_care_inst = aliased(ElderCareInstitution)
    funeral_inst = aliased(FuneralInstitution)

    # 查询养老机构
    managed_elder_care_institutions = db.session.query(elder_care_inst).join(
        StaffInstitution, elder_care_inst.InstitutionID == StaffInstitution.InstitutionID
    ).filter(StaffInstitution.UserID == user_id).all()

    # 查询殡葬机构
    managed_funeral_institutions = db.session.query(funeral_inst).join(
        StaffInstitution, funeral_inst.InstitutionID == StaffInstitution.InstitutionID
    ).filter(StaffInstitution.UserID == user_id).all()

    # 渲染模板并分别传递两个机构列表
    return render_template('manage_institution.html',
                           elder_care_institutions=managed_elder_care_institutions,
                           funeral_institutions=managed_funeral_institutions)


@institution_bp.route('/update_institution', methods=['POST'])
@login_required
def update_institution():
    data = request.json
    institution_id = data.get('institution_id')
    field = data.get('field')
    value = data.get('value')

    # 更新指定机构信息
    elder_institution = ElderCareInstitution.query.get(institution_id)
    funeral_institution = FuneralInstitution.query.get(institution_id)

    if elder_institution:
        setattr(elder_institution, field, value)
        db.session.commit()
        return jsonify({"status": "success", "message": "信息更新成功"})
    elif funeral_institution:
        setattr(funeral_institution, field, value)
        db.session.commit()
        return jsonify({"status": "success", "message": "信息更新成功"})
    else:
        return jsonify({"status": "error", "message": "机构未找到"}), 404


@institution_bp.route('/institution_reservations/<int:institution_id>')
@login_required
def institution_reservations(institution_id):
    # 获取机构的预约信息
    reservations = Reservation.query.filter_by(InstitutionID=institution_id).all()
    return jsonify([
        {
            "reservation_id": res.ReservationID,
            "user_id": res.UserID,
            "reservation_time": res.ReservationTime,
            "status": res.ReservationStatus,
        }
        for res in reservations
    ])


@institution_bp.route('/update_reservation_status', methods=['POST'])
@login_required
def update_reservation_status():
    data = request.json
    reservation_id = data.get('reservation_id')
    new_status = data.get('new_status')

    # 更新预约状态
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"status": "error", "message": "预约未找到"}), 404

    reservation.ReservationStatus = new_status
    db.session.commit()
    return jsonify({"status": "success", "message": "预约状态更新成功"})
