from extensions import db

class Reservation(db.Model):
    __tablename__ = 'reservation'

    ReservationID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, nullable=False)
    InstitutionID = db.Column(db.Integer, nullable=False)
    Role = db.Column(db.String(), nullable=False)
    ReservationTime = db.Column((db.DateTime), nullable=False)
    ReservationStatus = db.Column(db.Integer, nullable=True)

    # 外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(['UserID'], ['users.UserID']),
        db.ForeignKeyConstraint(['InstitutionID'], ['eldercareinstitution.InstitutionID']),
    )
