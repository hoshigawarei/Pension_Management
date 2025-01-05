from flask import redirect, Flask, Blueprint, render_template, request, jsonify, url_for, flash
from models.user import User, SeniorUser, FamilyCareGiver, FamilySeniorRelation
from models.eldercareinstitutionevaluation import ElderCareInstitutionEvaluation
from models.funeralinstitutionevaluation import FuneralInstitutionEvaluation
from models.staffinstitution import StaffInstitution
from models.userrole import UserRole
from models.healthdata import HeartRate  # 导入HeartRate模型
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required
from extensions import db


heartrate_bp = Blueprint('heartrate', __name__)

@heartrate_bp.route('/view_health_data', methods=['GET'])
@login_required
def view_heartrate():
    # 获取当前用户的角色
    user_role = UserRole.query.filter_by(UserID=current_user.UserID).first()

    # 如果是老年用户，查询并显示该用户的心率数据
    if user_role and user_role.Role == '老年用户':
        # 使用 JOIN 来关联 seniorhealthdata 和 SeniorUser 表
        health_data = db.session.query(HeartRate.HeartRate, SeniorUser.Residence,SeniorUser.RealName ).join(SeniorUser, SeniorUser.UserID == HeartRate.UserID).filter(HeartRate.UserID == current_user.UserID).first()
        
        # 如果没有找到心率数据，显示暂无数据
        if not health_data:
            flash("暂无心率数据", "info")
            heart_rate = None
            real_name=None
            residence = None
        else:
            heart_rate = health_data.HeartRate
            real_name=health_data.RealName
            residence = health_data.Residence
        
        # 渲染心率页面，传递心率数据和用户角色信息
        return render_template('heart_rate.html', heart_rate=heart_rate, real_name=real_name,residence=residence, user_role=user_role.Role)
    
    # 如果是家属、看护用户，查询并显示其关联的老年人的心率数据
    elif user_role and user_role.Role == '家属、看护用户':
        # 查询家属关联的老年人
        family_senior_relation = db.session.query(FamilySeniorRelation).filter(FamilySeniorRelation.FamilyCaregiverID

 == current_user.UserID).first()
    
        if family_senior_relation:
            # 查询老人的心率和住址
            health_data = db.session.query(HeartRate.HeartRate, SeniorUser.Residence, SeniorUser.RealName) \
                .join(SeniorUser, SeniorUser.UserID == HeartRate.UserID) \
                .filter(HeartRate.UserID == family_senior_relation.SeniorUserID) \
                .first()  # 获取老人的心率数据和住址

            if health_data:
                heart_rate = health_data.HeartRate
                real_name=health_data.RealName
                residence = health_data.Residence

            else:
                flash("该老年人暂无心率数据", "info")
                heart_rate = None
                real_name=None
                residence = None
        else:
             flash("没有找到关联的老年人", "info")
             heart_rate = None
             real_name=None
             residence = None
    
    # 渲染心率页面，传递心率数据和用户角色信息
        return render_template('heart_rate.html', heart_rate=heart_rate, real_name=real_name,residence=residence, user_role=user_role.Role)
                

    else:
        flash("你暂无权限查看此数据", "warning")
        return redirect(url_for('user.dashboard'))  # 跳转回用户仪表板