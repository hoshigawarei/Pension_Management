from extensions import db

class HeartRate(db.Model):
    __tablename__ = 'seniorhealthdata'

    UserID = db.Column(db.Integer, primary_key=True)
    HeartRate = db.Column(db.Integer, nullable=False)
