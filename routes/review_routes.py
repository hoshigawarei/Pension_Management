from flask import Flask, Blueprint, render_template, request, jsonify, url_for, flash
from models.user import User
from models.eldercareinstitutionevaluation import ElderCareInstitutionEvaluation
from models.funeralinstitutionevaluation import FuneralInstitutionEvaluation
from models.eldercareinstitution import ElderCareInstitution
from models.funeralinstitution import FuneralInstitution
from models.staffinstitution import StaffInstitution  # 导入StaffInstitution
from models.userrole import UserRole  # 导入UserRoles
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required
from extensions import db
from sqlalchemy.sql import func
from sqlalchemy import exists


review_bp = Blueprint('review', __name__)
report_bp = Blueprint('report', __name__)

# 查看评价
@review_bp.route('/evaluations/<int:InstitutionID>', methods=['GET'])
@login_required
def view_evaluations(InstitutionID):
    # 获取当前用户的角色
    user_role = UserRole.query.filter_by(UserID=current_user.UserID).first()

    # 判断机构类型并查询评价
    if InstitutionID in [institution.InstitutionID for institution in ElderCareInstitutionEvaluation.query.all()]:  # 判断是否为养老机构
        evaluations = ElderCareInstitutionEvaluation.query.filter_by(InstitutionID=InstitutionID).all()
    else:  # 否则为殡葬机构
        evaluations = FuneralInstitutionEvaluation.query.filter_by(InstitutionID=InstitutionID).all()

    # 如果没有评价，显示暂无
    if not evaluations:
        flash("暂无评价", "info")
    
    # 渲染评价模板，传递评价数据
    return render_template('evaluations.html', evaluations=evaluations, InstitutionID=InstitutionID, user_role=user_role)

# 查看举报信息
@review_bp.route('/report/<int:InstitutionID>', methods=['GET'])
@login_required
def view_reports(InstitutionID):
    # 获取当前用户的角色
    user_role = UserRole.query.filter_by(UserID=current_user.UserID).first()

    # 判断机构类型并查询举报信息
    if InstitutionID in [institution.InstitutionID for institution in ElderCareInstitutionEvaluation.query.all()]:  # 判断是否为养老机构
        # 查询含有举报信息的评价
        reports = ElderCareInstitutionEvaluation.query.filter_by(InstitutionID=InstitutionID).all()
    else:  # 否则为殡葬机构
        reports = FuneralInstitutionEvaluation.query.filter_by(InstitutionID=InstitutionID).all()

    # 如果没有举报信息，显示暂无
    if not reports:
        flash("暂无举报信息", "info")
    
    # 渲染模板，传递举报信息
    return render_template('reports.html', reports=reports, InstitutionID=InstitutionID, user_role=user_role)



# 提交评价
@review_bp.route('/institution/<int:InstitutionID>/review', methods=['POST'])
@login_required
def post_review(InstitutionID):
    # 获取当前用户的角色
    user_role = UserRole.query.filter_by(UserID=current_user.UserID).first()

    # 检查用户是否有权限提交评价
    if user_role is None or user_role.RoleID not in [2, 3]:  # 只有RoleID为2或3的用户可以对所有机构进行评价
        return jsonify({"status": "error", "message": "您没有权限进行评价"})

    # 机构管理人员只能对自己管理的机构进行评价
    if user_role.RoleID == 4:  # 机构管理人员
        # 查询该用户是否为该机构的管理人员
        managed_institution = db.session.query(StaffInstitution).filter_by(UserID=current_user.UserID, InstitutionID=InstitutionID).first()
        if not managed_institution:
            return jsonify({"status": "error", "message": "您没有权限评价此机构"})

    # 获取提交的评价内容
    review_content = request.form.get('review_content')
    review_score = request.form.get('review_score')

    if not review_content or not review_score:
        flash("评价内容和评分不能为空", "danger")
        return jsonify({"status": "error", "message": "评价内容和评分不能为空"})

    # 创建新的评价记录
    if db.session.query(exists().where(ElderCareInstitution.InstitutionID == int(InstitutionID))).scalar():  # 养老机构
        # 获取当前最大 EvaluationID
        max_id = db.session.query(func.max(ElderCareInstitutionEvaluation.EvaluationID)).scalar()
        next_id = max_id + 1 if max_id is not None else 300001

        review = ElderCareInstitutionEvaluation(
            EvaluationID=next_id,
            UserID=current_user.UserID,
            InstitutionID=InstitutionID,
            Evaluation=review_content,
            Rating=review_score,
            ReportInfo=None
        )
    elif db.session.query(exists().where(FuneralInstitution.InstitutionID == InstitutionID)).scalar():  # 殡葬机构
        # 获取当前最大 EvaluationID
        max_id = db.session.query(func.max(FuneralInstitutionEvaluation.EvaluationID)).scalar()
        next_id = max_id + 1 if max_id is not None else 310001

        review = FuneralInstitutionEvaluation(
            EvaluationID=next_id,
            UserID=current_user.UserID,
            InstitutionID=InstitutionID,
            Evaluation=review_content,
            Rating=review_score,
            ReportInfo=None
        )

    # 将评价保存到数据库
    db.session.add(review)
    db.session.commit()

    flash("评价提交成功", "success")
    return jsonify({"status": "success", "message": "评价提交成功"})

# 提交举报
@review_bp.route('/institution/<int:InstitutionID>/report', methods=['POST'])
@login_required
def post_report(InstitutionID):
    # 获取当前用户的角色
    user_role = UserRole.query.filter_by(UserID=current_user.UserID).first()

    # 检查用户是否有权限提交举报
    if user_role is None or user_role.RoleID not in [1, 2, 3, 5]:  # 只有RoleID为1、2、3、5的用户可以提交举报
        return jsonify({"status": "error", "message": "您没有权限提交举报"})

    # 获取提交的举报信息
    report_content = request.form.get('report_content')

    if not report_content:
        flash("举报内容不能为空", "danger")
        return jsonify({"status": "error", "message": "举报内容不能为空"})

    # 创建新的举报记录
    if db.session.query(exists().where(ElderCareInstitution.InstitutionID == int(InstitutionID))).scalar():  # 养老机构
         # 获取当前最大 EvaluationID
        max_id = db.session.query(func.max(ElderCareInstitutionEvaluation.EvaluationID)).scalar()
        next_id = max_id + 1 if max_id is not None else 300001
        report = ElderCareInstitutionEvaluation(
            EvaluationID=next_id,
            UserID=current_user.UserID,
            InstitutionID=InstitutionID,
            Evaluation=None,
            Rating=None,
            ReportInfo=report_content  # 提交举报内容
        )
    elif db.session.query(exists().where(FuneralInstitution.InstitutionID == InstitutionID)).scalar():  # 殡葬机构
         # 获取当前最大 EvaluationID
        max_id = db.session.query(func.max( FuneralInstitutionEvaluation.EvaluationID)).scalar()
        next_id = max_id + 1 if max_id is not None else 310001
        report = FuneralInstitutionEvaluation(
            EvaluationID=next_id,
            UserID=current_user.UserID,
            InstitutionID=InstitutionID,
            Evaluation=None,
            Rating=None,
            ReportInfo=report_content  # 提交举报内容
        )


    # 将举报记录保存到数据库
    db.session.add(report)
    db.session.commit()

    flash("举报提交成功", "success")
    return jsonify({"status": "success", "message": "举报提交成功"})
