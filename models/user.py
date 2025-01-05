from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(255), nullable=False)  # 存储加密后的密码
    PhoneNumber = db.Column(db.String(15), nullable=False)

    roles = db.relationship('UserRole', back_populates='user')  # 反向关系

    def __repr__(self):
        return f"<User {self.Username}>"
    
    # 显式覆盖 get_id() 方法
    def get_id(self):
        return str(self.UserID)
    
class SeniorUser(db.Model):
    __tablename__ = 'senioruser'
    UserID = db.Column(db.Integer, primary_key=True)
    RealName = db.Column(db.String(20), nullable=False)
    IDNumber = db.Column(db.String(18), nullable=False)
    Residence = db.Column(db.String(50), nullable=False)

        # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['UserID'], ['users.UserID']),
    )

class FamilyCareGiver(db.Model):
    __tablename__ = 'familycaregiver'
    UserID = db.Column(db.Integer, primary_key=True)
    RealName = db.Column(db.String(20), nullable=False)
    IDNumber = db.Column(db.String(18), nullable=False)

        # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['UserID'], ['users.UserID']),
    )

class FamilySeniorRelation(db.Model):
    __tablename__ = 'familyseniorrelation'

    # 定义联合主键
    FamilyCaregiverID= db.Column(db.Integer, primary_key=True)
    SeniorUserID = db.Column(db.Integer, primary_key=True)

    # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['FamilyCaregiverID'], ['users.UserID']),
        db.ForeignKeyConstraint(['SeniorUserID'], ['users.UserID']),
    )

class Staff(db.Model):
    __tablename__ = 'staff'
    UserID = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.String(20), primary_key=True)

        # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['UserID'], ['users.UserID']),
    )

class Supervisor(db.Model):
    __tablename__ = 'supervisor'
    UserID = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.String(20), nullable=False)
    EmployeeNumber = db.Column(db.String(20), nullable=False)

        # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['UserID'], ['users.UserID']),
    )