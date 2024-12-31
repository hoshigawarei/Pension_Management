from extensions import db

class FuneralInstitution(db.Model):
    __tablename__ = 'funeralinstitution'

    InstitutionID = db.Column(db.Integer, primary_key=True)
    InstitutionName = db.Column(db.String(50), unique=True, nullable=False)
    Address = db.Column(db.String(100), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(15), nullable=False)
    PostalCode = db.Column(db.String(10))
    ContactPerson = db.Column(db.String(20), nullable=False)
    InstitutionType = db.Column(db.String(20), nullable=False)
    ServiceScope = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<FuneralInstitution {self.InstitutionName}>"

    def to_dict(self):
        """将实例转换为字典格式"""
        return {
            "InstitutionID": self.InstitutionID,
            "InstitutionName": self.InstitutionName,
            "Address": self.Address,
            "PhoneNumber": self.PhoneNumber,
            "PostalCode": self.PostalCode,
            "ContactPerson":self.ContactPerson,
            "InstitutionType":self.InstitutionType,
            "ServiceScope":self.ServiceScope
        }