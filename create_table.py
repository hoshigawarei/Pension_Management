import mysql.connector
from db_config import DB_CONFIG

conn = mysql.connector.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)

cursor = conn.cursor()
cursor.execute("USE pension_management;")  # 选择数据库

# 创建 Users 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID INT PRIMARY KEY,
        Username VARCHAR(20) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        PhoneNumber VARCHAR(15) NOT NULL
    );
""")

# 创建 UserRoles 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS UserRoles (
       UserID INT PRIMARY KEY,
       RoleID INT NOT NULL,
       Role VARCHAR(10) NOT NULL,
       FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# 创建 GeneralUser 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS GeneralUser (
       UserID INT PRIMARY KEY,
       FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# 创建 SeniorUser 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SeniorUser (
       UserID INT PRIMARY KEY,
       RealName VARCHAR(20) NOT NULL,
       IDNumber VARCHAR(18) NOT NULL,
       Residence VARCHAR(50) NOT NULL,
       FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# 创建 SeniorHealthData 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SeniorHealthData (
       UserID INT PRIMARY KEY,
       HeartRate INT NOT NULL,
       FOREIGN KEY (UserID) REFERENCES SeniorUser(UserID)
    );
""")

# 创建 FamilyCaregiver 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FamilyCaregiver (
       UserID INT PRIMARY KEY,
       RealName VARCHAR(20) NOT NULL,
       IDNumber VARCHAR(18) NOT NULL,
       FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# 创建 FamilySeniorRelation 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FamilySeniorRelation (
       FamilyCaregiverID INT,
       SeniorUserID INT,
       PRIMARY KEY (FamilyCaregiverID, SeniorUserID),
       FOREIGN KEY (FamilyCaregiverID) REFERENCES FamilyCaregiver(UserID),
       FOREIGN KEY (SeniorUserID) REFERENCES SeniorUser(UserID)
    );
""")

# 创建 Staff 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Staff (
       UserID INT,
       Position VARCHAR(20),
       PRIMARY KEY (UserID, Position),
       FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# 创建 Supervisor 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Supervisor (
       UserID INT PRIMARY KEY,
       Position VARCHAR(20) NOT NULL,
       EmployeeNumber VARCHAR(20) NOT NULL,
       FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# 创建 ElderCareInstitution 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ElderCareInstitution (
       InstitutionID INT PRIMARY KEY,
       StreetTown VARCHAR(50) NOT NULL,
       InstitutionName VARCHAR(50) UNIQUE,
       BedCount INT NOT NULL,
       OperationYearMonth VARCHAR(50) NOT NULL,
       Address VARCHAR(100) NOT NULL,
       PhoneNumber VARCHAR(15) NOT NULL,
       PostalCode VARCHAR(10),
       OperationMode VARCHAR(10) NOT NULL,
       LegalRepresentative VARCHAR(20) NOT NULL
    );
""")

# 创建 FuneralInstitution 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FuneralInstitution (
       InstitutionID INT PRIMARY KEY,
       InstitutionName VARCHAR(50) UNIQUE,
       Address VARCHAR(100) UNIQUE,
       PhoneNumber VARCHAR(15) NOT NULL,
       PostalCode VARCHAR(10) ,
       ContactPerson VARCHAR(20) NOT NULL,
       InstitutionType VARCHAR(20) NOT NULL,
       ServiceScope VARCHAR(50) NOT NULL
    );
""")

# 创建 StaffInstitution 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS StaffInstitution (
       UserID INT,
       InstitutionID INT,
       PRIMARY KEY (UserID, InstitutionID),
       FOREIGN KEY (UserID) REFERENCES Staff(UserID),
       FOREIGN KEY (InstitutionID) REFERENCES ElderCareInstitution(InstitutionID)
    );
""")

# 创建 ElderCareInstitutionEvaluation 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ElderCareInstitutionEvaluation (
       EvaluationID INT PRIMARY KEY,
       UserID INT NOT NULL,
       InstitutionID INT NOT NULL,
       Evaluation TEXT NOT NULL,
       Rating INT,
       ReportInfo TEXT,
       FOREIGN KEY (InstitutionID) REFERENCES ElderCareInstitution(InstitutionID)
    );
""")

# 创建 FuneralInstitutionEvaluation 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FuneralInstitutionEvaluation (
       EvaluationID INT PRIMARY KEY,
       UserID INT NOT NULL,
       InstitutionID INT NOT NULL,
       Evaluation TEXT NOT NULL,
       Rating INT,
       ReportInfo TEXT,
       FOREIGN KEY (InstitutionID) REFERENCES FuneralInstitution(InstitutionID)
    );
""")

# 创建 Reservation 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reservation (
       ReservationID INT PRIMARY KEY,
       UserID INT NOT NULL,
       InstitutionID INT NOT NULL,
       Role VARCHAR(10) NOT NULL,
       ReservationTime DATETIME NOT NULL,
       ReservationStatus INT CHECK (ReservationStatus IN (1, 2, 3, 4)),
       FOREIGN KEY (UserID) REFERENCES Users(UserID),
       FOREIGN KEY (InstitutionID) REFERENCES ElderCareInstitution(InstitutionID)
    );
""")

# 创建 EmergencyCall 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS EmergencyCall (
       EmergencyCallID INT PRIMARY KEY,
       SeniorUserID INT NOT NULL,
       CallType VARCHAR(4) CHECK (CallType IN ('self', 'auto')),
       FOREIGN KEY (SeniorUserID) REFERENCES SeniorUser(UserID)
    );
""")

# 创建 EmergencyCallUser 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS EmergencyCallUser (
       EmergencyCallID INT,
       FamilyCaregiverID INT,
       HeartRate TEXT NOT NULL,
       PRIMARY KEY (EmergencyCallID, FamilyCaregiverID),
       FOREIGN KEY (EmergencyCallID) REFERENCES EmergencyCall(EmergencyCallID),
       FOREIGN KEY (FamilyCaregiverID) REFERENCES FamilyCaregiver(UserID)
    );
""")

#  创建 Permissions 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Permissions (
       PermissionID INT PRIMARY KEY,
       PermissionName VARCHAR(50) NOT NULL,
       PermissionDescription VARCHAR(50) NOT NULL     
    );
""")

#  创建 RolePermissions 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS RolePermissions (
       RoleID INT NOT NULL,
       PermissionID INT NOT NULL,
       FOREIGN KEY (RoleID) REFERENCES UserRoles(RoleID),
       FOREIGN KEY (PermissionID) REFERENCES Permissions(PermissionID)            
    );
""")

print("表格创建成功！")

cursor.close()
conn.close()
