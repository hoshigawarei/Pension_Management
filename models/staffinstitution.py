from extensions import db

# 机构管理人员与机构的关系表
class StaffInstitution(db.Model):
    __tablename__ = 'staffinstitution'
    
    UserID = db.Column(db.Integer, primary_key=True)  # 用户 ID（管理人员）
    InstitutionID = db.Column(db.Integer, primary_key=True)  # 机构 ID

    # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['UserID'], ['staff.UserID']),
        db.ForeignKeyConstraint(['InstitutionID'], ['eldercareinstitution.InstitutionID']),
    )