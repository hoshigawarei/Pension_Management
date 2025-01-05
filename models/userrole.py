from extensions import db

class UserRole(db.Model):
    __tablename__ = 'UserRoles'
    
    # 主键
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), primary_key=True)
    RoleID = db.Column(db.Integer, nullable=False)
    Role = db.Column(db.String(10), nullable=False)

    # 定义外键关系
    user = db.relationship('User', backref=db.backref('user_roles', lazy=True))

    def __repr__(self):
        return f"<UserRole UserID={self.UserID}, Role={self.Role}>"
