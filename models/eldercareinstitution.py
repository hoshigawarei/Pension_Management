from extensions import db

class ElderCareInstitution(db.Model):
    __tablename__ = 'eldercareinstitution'

    InstitutionID = db.Column(db.Integer, primary_key=True)
    InstitutionName = db.Column(db.String(50), unique=True, nullable=False)
    StreetTown = db.Column(db.String(50), nullable=False)
    BedCount = db.Column(db.Integer, nullable=False)
    OperationYearMonth = db.Column(db.String(50), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    PhoneNumber = db.Column(db.String(15), nullable=False)
    PostalCode = db.Column(db.String(10))
    OperationMode = db.Column(db.String(10), nullable=False)
    LegalRepresentative = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<ElderCareInstitution {self.InstitutionName}>"
    
    def to_dict(self):
        """将实例转换为字典格式"""
        return {
            "InstitutionID": self.InstitutionID,
            "InstitutionName": self.InstitutionName,
            "StreetTown": self.StreetTown,
            "BedCount": self.BedCount,
            "OperationYearMonth": self.OperationYearMonth,
            "Address": self.Address,
            "PhoneNumber": self.PhoneNumber,
            "PostalCode": self.PostalCode,
            "OperationMode": self.OperationMode,
            "LegalRepresentative": self.LegalRepresentative
        }
