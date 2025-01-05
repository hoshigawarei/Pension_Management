from flask import redirect, Flask, Blueprint, render_template, request, jsonify, url_for, flash
from models.user import User, SeniorUser, FamilyCareGiver, FamilySeniorRelation
from models.eldercareinstitutionevaluation import ElderCareInstitutionEvaluation
from models.funeralinstitutionevaluation import FuneralInstitutionEvaluation
from models.staffinstitution import StaffInstitution
from models.userrole import UserRole
from models.healthdata import HeartRate  # 导入HeartRate模型
from models.emergencycall import EmergencyCall, EmergencyCallUser
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required
from extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload

emergencycall_bp = Blueprint('emergencycall', __name__)

@emergencycall_bp.route('/emergency_call', methods=['GET', 'POST'])
@login_required
def manage_emergency_call():
    # 确认当前用户是老年用户
    user_role = db.session.query(UserRole).filter_by(UserID=current_user.UserID).first()
    if not user_role or user_role.Role != '老年用户':
        flash("您没有权限访问此页面。", "warning")
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'GET':
        print("Request method:", request.method)
        # 查询当前用户的所有呼救记录
        emergency_calls = db.session.query(EmergencyCall).filter_by(SeniorUserID=current_user.UserID).all()
        return render_template('emergency_calls.html', emergency_calls=emergency_calls)
    
    if request.method == 'POST':
        print("Request method:", request.method)
        # 获取当前最大 EmergencyCallID
        max_id = db.session.query(func.max(EmergencyCall.EmergencyCallID)).scalar()
        next_id = max_id + 1 if max_id is not None else 500001

        # 创建新的呼救记录
        new_call = EmergencyCall(
            EmergencyCallID=next_id,
            SeniorUserID=current_user.UserID,
            CallType='self'
        )

        FamilyCaregiver_ID=db.session.query(FamilySeniorRelation).filter_by(SeniorUserID=current_user.UserID).first()
        Heart_Rate=db.session.query(HeartRate).filter_by(UserID=current_user.UserID).first()

        new_callUser = EmergencyCallUser(
            EmergencyCallID = next_id, 
            FamilyCaregiverID = FamilyCaregiver_ID.FamilyCaregiverID, 
            HeartRate =  Heart_Rate.HeartRate
        )

        try:
            db.session.add(new_call)
            db.session.add(new_callUser)
            db.session.commit()
            print(f"Success")  # 或使用 logging 记录
            flash("自动呼救记录已成功添加！", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # 或使用 logging 记录
            flash(f"呼救记录添加失败: {e}", "danger")

        return redirect(url_for('emergencycall.manage_emergency_call'))
    
@emergencycall_bp.route('/view_emergency_call', methods=['GET'])
@login_required
def view_emergency_call():
    # 确认当前用户是家属用户
    user_role = db.session.query(UserRole).filter_by(UserID=current_user.UserID).first()
    if not user_role or user_role.Role != '家属、看护用户':
        flash("您没有权限访问此页面。", "warning")
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'GET':
        print("Request method:", request.method)
        # 查询当前绑定用户的所有呼救记录
        # 查询绑定用户的所有呼救记录以及相关信息
        emergency_calls = (
            db.session.query(
                EmergencyCallUser.EmergencyCallID,
                EmergencyCallUser.HeartRate,
                EmergencyCall.SeniorUserID,
                SeniorUser.RealName,
                SeniorUser.Residence,
            )
            .join(EmergencyCall, EmergencyCallUser.EmergencyCallID == EmergencyCall.EmergencyCallID)
            .join(SeniorUser, EmergencyCall.SeniorUserID == SeniorUser.UserID)
            .filter(EmergencyCallUser.FamilyCaregiverID
 == current_user.UserID)
            .all()
        )
        return render_template('view_emergency_calls.html', emergency_calls=emergency_calls)
    