from extensions import db

class EmergencyCall(db.Model):
    __tablename__ = 'emergencycall'

    EmergencyCallID = db.Column(db.Integer, primary_key=True)
    SeniorUserID = db.Column(db.Integer, nullable=False)
    CallType = db.Column(db.String(4))

    __table_args__ = (
        db.ForeignKeyConstraint(['SeniorUserID'], ['senioruser.UserID']),
    )    

class EmergencyCallUser(db.Model):
    __tablename__ = 'emergencycalluser'
    EmergencyCallID= db.Column(db.Integer, primary_key=True)
    FamilyCaregiverID=db.Column(db.Integer, primary_key=True)
    HeartRate=db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(['EmergencyCallID'], ['emergencycall.EmergencyCallID']),
        db.ForeignKeyConstraint(['FamilyCaregiverID'], ['familycaregiver.UserID']),
    ) 