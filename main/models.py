from datetime import date,datetime,time
from flask_login import UserMixin
from main import db
from main import login_manager


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(50),unique=True)
	full_name = db.Column(db.String(100))
	department = db.Column(db.String(225))
	student_id = db.Column(db.String(25))
	password = db.Column(db.String(100), nullable=False)
	user_type = db.Column(db.String(100))
	lessons = db.relationship('Lessons',backref='user',lazy=True)
	hometask = db.relationship('Hometask',backref='user',lazy=True)
	solution = db.relationship('Solution',backref='user',lazy=True)
	def __repr__ (self):
		return f"User('{self.username}')"


class Lessons(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	lesson_name = db.Column(db.String(100),nullable=False)
	lesson_description = db.Column(db.String(500))
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	attachment = db.Column(db.String(500))
	teacherId = db.Column(db.Integer,db.ForeignKey("user.id"))
	subjectId = db.Column(db.Integer,db.ForeignKey("subjects.id"))
	majorId = db.Column(db.Integer,db.ForeignKey("majors.id"))
	attachments = db.relationship('Attachments',backref='lessons',lazy=True)


class Reference(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	reference_name = db.Column(db.String(100),nullable=False)
	reference_description = db.Column(db.String(500))
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	attachment = db.Column(db.String(500))
	teacherId = db.Column(db.Integer,db.ForeignKey("user.id"))
	majorId = db.Column(db.Integer,db.ForeignKey("majors.id"))


class Subjects(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject_name = db.Column(db.String(100),nullable=False)
	lessons = db.relationship('Lessons',backref='subjects',lazy=True)
	hometask = db.relationship('Hometask',backref='subjects',lazy=True)


class Majors(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	major_name = db.Column(db.String(100),nullable=False)
	lessons = db.relationship('Lessons',backref='majors',lazy=True)
	hometask = db.relationship('Hometask',backref='majors',lazy=True)


class Attachments(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	filename = db.Column(db.String(100),nullable=False)
	attachment = db.Column(db.String(500))
	lesson_id = db.Column(db.Integer,db.ForeignKey("lessons.id"))


class Hometask(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	hometask_name = db.Column(db.String(100),nullable=False)
	hometask_description = db.Column(db.String(500))
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	attachment = db.Column(db.String(500))
	teacherId = db.Column(db.Integer,db.ForeignKey("user.id"))
	majorId = db.Column(db.Integer,db.ForeignKey("majors.id"))
	subjectId = db.Column(db.Integer,db.ForeignKey("subjects.id"))
	solution = db.relationship('Solution',backref='hometask',lazy=True)


class Solution(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	solution_name = db.Column(db.String(100),nullable=False)
	solution_description = db.Column(db.String(500))
	completed = db.Column(db.Boolean)
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	attachment = db.Column(db.String(500))
	studentId = db.Column(db.Integer,db.ForeignKey("user.id"))
	hometaskId = db.Column(db.Integer,db.ForeignKey("hometask.id"))