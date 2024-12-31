from extensions import db

# 殡葬机构评价表
class FuneralInstitutionEvaluation(db.Model):
    __tablename__ = 'funeralinstitutionevaluation'
    
    EvaluationID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    UserID = db.Column(db.Integer, nullable=False)  # 用户 ID
    InstitutionID = db.Column(db.Integer, nullable=False)  # 机构 ID
    Evaluation = db.Column(db.Text, nullable=True)  # 评价内容
    Rating = db.Column(db.Integer, nullable=True)  # 评分
    ReportInfo = db.Column(db.Text, nullable=True)  # 举报信息

    # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['InstitutionID'], ['funeralinstitution.InstitutionID']),
    )