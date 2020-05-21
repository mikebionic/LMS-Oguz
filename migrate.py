from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from forms import PostLessonForm,UploadFileForm

from datetime import date,datetime,time
app = Flask (__name__)
app.config['SECRET_KEY'] = "sdffggohr30ifrnf3e084fn0348"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lessonsShare.db'

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

class Subjects(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject_name = db.Column(db.String(100),nullable=False)
	lessons = db.relationship('Lessons',backref='subjects',lazy=True)

class Majors(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	major_name = db.Column(db.String(100),nullable=False)
	lessons = db.relationship('Lessons',backref='majors',lazy=True)

# #### auth and login routes ####
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(50),unique=True,nullable =False)
	full_name = db.Column(db.String(100))
	password = db.Column(db.String(100), nullable=False)
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

major = Majors(major_name="Maglumat Ulgamlary we Tehnologiyalary")
db.session.add(major)
major = Majors(major_name="Informatika we hasaplayys tehnikasy")
db.session.add(major)
major = Majors(major_name="Innowatika")
db.session.add(major)
major = Majors(major_name="Biotehnologiya")
db.session.add(major)
major = Majors(major_name="Awtomatlastyrmak we dolandyrmak")
db.session.add(major)

db.session.commit()

# if __name__ == "__main__":
# 	app.run(host="0.0.0.0" , port=5000 , debug=True)