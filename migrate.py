from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from forms import PostLessonForm,UploadFileForm

from datetime import date,datetime,time
app = Flask (__name__)
app.config['SECRET_KEY'] = "sdffggohr30ifrnf3e084fn0348"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'

db = SQLAlchemy(app)
# #### lessons db and CRUD #####

### lesson models ###

class Lessons(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	lesson_name = db.Column(db.String(100),nullable =False)
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	attachment = db.Column(db.String(500))
	teacherId = db.Column(db.Integer,db.ForeignKey("user.id"))
	subjectId = db.Column(db.Integer,db.ForeignKey("subjects.id"))
	majorId = db.Column(db.Integer,db.ForeignKey("majors.id"))
	attachments = db.relationship('Attachments',backref='lessons',lazy=True)

class Subjects(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject_name = db.Column(db.String(100),nullable=False)
	lessons = db.relationship('Lessons',backref='subjects',lazy=True)

class Majors(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	major_name = db.Column(db.String(100),nullable=False)
	lessons = db.relationship('Lessons',backref='majors',lazy=True)

class Attachments(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	filename = db.Column(db.String(100),nullable=False)
	attachment = db.Column(db.String(500))
	lesson_id = db.Column(db.Integer,db.ForeignKey("lessons.id"))

# #### auth and login routes ####
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(50),unique=True)
	full_name = db.Column(db.String(100))
	department = db.Column(db.String(225))
	student_id = db.Column(db.String(25))
	password = db.Column(db.String(100),nullable=False)
	user_type = db.Column(db.String(100))
	lessons = db.relationship('Lessons',backref='user',lazy=True)
	def __repr__ (self):
		return f"User('{self.username}')"

db.drop_all()
db.create_all()

subject = Subjects(subject_name="Computer Programming")
db.session.add(subject)
subject = Subjects(subject_name="Web programming Practice")
db.session.add(subject)
subject = Subjects(subject_name="Computer Network")
db.session.add(subject)
subject = Subjects(subject_name="Political Science")
db.session.add(subject)
subject = Subjects(subject_name="Artificial Intelligence")
db.session.add(subject)
subject = Subjects(subject_name="Mobile device Programming")
db.session.add(subject)


major = Majors(major_name="Awtomatlastyrmak we dolandyrmak")
db.session.add(major)
major = Majors(major_name="Mehatronika we robot tehnikasy")
db.session.add(major)
major = Majors(major_name="Elektronika we nanoelektronika")
db.session.add(major)
major = Majors(major_name="Maglumat Ulgamlary we Tehnologiyalary")
db.session.add(major)
major = Majors(major_name="Informatika we hasaplayys tehnikasy")
db.session.add(major)
major = Majors(major_name="Animasiya we grafika dizayny")
db.session.add(major)
major = Majors(major_name="Sanly ykdysadyyet")
db.session.add(major)
major = Majors(major_name="Innowatika")
db.session.add(major)
major = Majors(major_name="Biotehnologiya")
db.session.add(major)
major = Majors(major_name="Nanotehnologiyalar we nanomateriallar")
db.session.add(major)
major = Majors(major_name="Materiallaryn tehnologiyalary")
db.session.add(major)
major = Majors(major_name="Himiki tehnologiyalar")
db.session.add(major)
major = Majors(major_name="Ekologiya we tebigatdan peydalanmak")
db.session.add(major)
major = Majors(major_name="Genetika we bioinziniring")
db.session.add(major)

# Required admin user

admin = User(username="administrator",password="lms_system@root/key",
	user_type="admin",full_name="Administrator")
db.session.add(admin)

# Exaple user insertions

student = User(username="student",password="123",student_id="134543",
	user_type="student",full_name="Ata Atajanow")
db.session.add(student)

teacher = User(username="plan",password="123",
	user_type="teacher",full_name="Plan Planyyew",department="Innowatika")
db.session.add(teacher)
teacher = User(username="saryyewd",password="DS2222",
	user_type="teacher",full_name="Döwlet Saryýew",department="Sanly ykdysadyýet")
db.session.add(teacher)
teacher = User(username="akgayewa",password="AA3333",
	user_type="teacher",full_name="Ahal Akgaýew",department="Kompýuter ylymlary we tehnologiýalary")
db.session.add(teacher)
teacher = User(username="akmyradovaa",password="AA4444",
	user_type="teacher",full_name="Aýlar Akmyradowa",department="Kompýuter ylymlary we tehnologiýalary")
db.session.add(teacher)
                    

db.session.commit()