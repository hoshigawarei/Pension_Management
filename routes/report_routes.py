from flask import Flask, Blueprint, render_template, request, jsonify, url_for,redirect, flash
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


# 判断机构类型并查询评价
def get_institution_type_by_id(institutionid):
    # 判断是否为养老机构
    elder_institution = ElderCareInstitutionEvaluation.query.filter_by(InstitutionID=institutionid).first()
    if elder_institution:
        return 'elder', elder_institution

    # 判断是否为殡葬机构
    funeral_institution = FuneralInstitutionEvaluation.query.filter_by(InstitutionID=institutionid).first()
    if funeral_institution:
        return 'funeral', funeral_institution

    return None, None  # 如果没有找到，返回 None


manage_report_bp = Blueprint('manage_report', __name__)
# 管理举报信息页面
@manage_report_bp.route('/manage_report', methods=['GET'])
@login_required
def manage_report():
    # 查询所有的养老机构和殡葬机构的举报，并获取机构名称
    elder_reports = ElderCareInstitutionEvaluation.query.filter(ElderCareInstitutionEvaluation.ReportInfo.isnot(None)).all()
    funeral_reports = FuneralInstitutionEvaluation.query.filter(FuneralInstitutionEvaluation.ReportInfo.isnot(None)).all()

    # 获取机构名称
    elder_institution_names = {}
    for report in elder_reports:
        institution = ElderCareInstitution.query.filter_by(InstitutionID=report.InstitutionID).first()
        elder_institution_names[report.InstitutionID] = institution.InstitutionName if institution else '未知'

    funeral_institution_names = {}
    for report in funeral_reports:
        institution = FuneralInstitution.query.filter_by(InstitutionID=report.InstitutionID).first()
        funeral_institution_names[report.InstitutionID] = institution.InstitutionName if institution else '未知'

    # 渲染举报信息页面
    return render_template('manage_report.html', elder_reports=elder_reports, funeral_reports=funeral_reports,
                           elder_institution_names=elder_institution_names, funeral_institution_names=funeral_institution_names)

@manage_report_bp.route('/edit_report/<int:InstitutionID>/<int:EvaluationID>', methods=['GET', 'POST'])
@login_required
def edit_report(InstitutionID,EvaluationID):
    institution_type, institution = get_institution_type_by_id(InstitutionID)
    
    if institution is None:
        return "Institution not found", 404

    # 获取机构名称
    if institution_type == 'elder':
        institution_name = ElderCareInstitution.query.filter_by(InstitutionID=InstitutionID).first().InstitutionName
        report_info = ElderCareInstitutionEvaluation.query.filter_by(EvaluationID=EvaluationID).first().ReportInfo

    elif institution_type == 'funeral':
        institution_name = FuneralInstitution.query.filter_by(InstitutionID=InstitutionID).first().InstitutionName
        report_info = FuneralInstitutionEvaluation.query.filter_by(EvaluationID=EvaluationID).first().ReportInfo

    # 如果是 GET 请求，显示现有的举报信息
    if request.method == 'GET':
        return render_template('edit_report.html', report_info=report_info, institution_type=institution_type,
                               institution_name=institution_name)

    # 如果是 POST 请求，更新举报信息
    new_report_info = request.form['report_info']
    
    # 根据机构类型更新举报信息
    if institution_type == 'elder':
        report = ElderCareInstitutionEvaluation.query.filter_by(EvaluationID=EvaluationID).first()
        if report:  # 如果报告存在，更新举报信息
            report.ReportInfo = new_report_info
    elif institution_type == 'funeral':
        report = FuneralInstitutionEvaluation.query.filter_by(EvaluationID=EvaluationID).first()
        if report:  # 如果报告存在，更新举报信息
            report.ReportInfo = new_report_info

    # 提交更新到数据库
    db.session.commit()

    return redirect(url_for('manage_report.manage_report'))

# 删除报告信息（仅清空 ReportInfo 字段）
@manage_report_bp.route('/delete_report/<int:InstitutionID>/<int:EvaluationID>', methods=['GET'])
@login_required
def delete_report(InstitutionID,EvaluationID):
    institution_type, institution = get_institution_type_by_id(InstitutionID)
    
    if institution is None:
        return "Institution not found", 404
    
    if institution_type == 'elder':
        report = ElderCareInstitutionEvaluation.query.filter_by(EvaluationID=EvaluationID).first()
        report.ReportInfo = None
    elif institution_type == 'funeral':
        report = FuneralInstitutionEvaluation.query.filter_by(EvaluationID=EvaluationID).first()
        report.ReportInfo = None
        
    db.session.commit()

    return redirect(url_for('manage_report.manage_report'))

