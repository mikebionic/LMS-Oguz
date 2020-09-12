from flask import Flask,render_template,url_for,flash,redirect,request,Response,abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from forms import PostLessonForm,UploadFileForm

# ### imports for file operations
import os,secrets
from PIL import Image
from werkzeug.utils import secure_filename
from importlib import import_module
########################


from datetime import date,datetime,time
app = Flask (__name__)
UPLOAD_FOLDER = 'static/post_uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "sdffggohr30ifrnf3e084fn0348"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'main'
login_manager.login_message = 'Programma girin!'
login_manager.login_message_category = 'info'


# #### lessons db and CRUD #####

### lesson models ###

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

###  end of lesson models ###


#### interactive pages of view ####

def save_attachment(form_attachment):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_attachment.filename)
	attachment_fn = random_hex + f_ext
	attachment_path = os.path.join(app.root_path, 'static/attachments/', attachment_fn)
	print('attachment_path')
	form_attachment.save(attachment_path)
	print('saved')
	return attachment_fn

@app.route("/teacher",methods=['GET','POST'])
@login_required
def teacher():
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	form = PostLessonForm()
	majors = Majors.query.all()
	subjects = Subjects.query.all()

	if request.method == 'GET':
		try:
			lessons = Lessons.query.filter_by(teacherId=current_user.id)
		except:
			lessons = Lessons.query.all()
		majors = Majors.query.all()
		subjects = Subjects.query.all()
		return render_template ("teacher/teacher.html",
			lessons=lessons,subjects=subjects,majors=majors,form=form)
	if request.method == 'POST':
		# if form.validate_on_submit():
		lesson = {
			'lesson_name':form.lesson_name.data,
			'lesson_description':form.lesson_description.data,
			'subjectId':form.subject.data,
			'majorId':form.major.data,
			'teacherId':current_user.id
		}
		if form.attachment.data:
			attachment_file = save_attachment(form.attachment.data)
			lesson.update({'attachment':attachment_file})
		newLesson = Lessons(**lesson)
		db.session.add(newLesson)
		db.session.commit()
		flash('Lesson successfully added', 'success')
		return redirect('/teacher')
	return render_template ("teacher/teacher.html",subjects=subjects,majors=majors,form=form)

@app.route("/lessons/attach/<int:lessonId>",methods=['GET','POST'])
@login_required
def attach(lessonId):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	lesson = Lessons.query.get(lessonId)
	form = AddAttachmentForm()
	if request.method == 'POST':
		# if form.validate_on_submit():
		try:
			attachment = {
				'filename':form.filename.data,
				'lesson_id':lessonId
			}
			if form.attachment.data:
				attachment_file = save_attachment(form.attachment.data)
				attachment.update({'attachment':attachment_file})
			newAttachment = Attachments(**attachment)
			db.session.add(newAttachment)
			db.session.commit()
			flash('Attachment successfully uploaded', 'success')
		except Exception as ex:
			print(ex)
		return redirect('/lessons/edit/'+str(lessonId))
	return render_template("teacher/add_attachment.html",lesson=lesson,form=form)

@app.route("/lessons/attach/<int:lessonId>/delete/<int:attachment_id>",methods=['GET'])
@login_required
def delete_attachment(lessonId,attachment_id):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	attachment = Attachments.query.get(attachment_id)
	db.session.delete(attachment)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/lessons/edit/'+str(lessonId))

@app.route("/lessons/delete/<int:lessonId>",methods=['GET'])
@login_required
def delete_lesson(lessonId):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	lesson = Lessons.query.get(lessonId)
	db.session.delete(lesson)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/teacher')

@app.route("/lessons/edit/<int:lessonId>",methods=['GET','POST'])
@login_required
def edit_lesson(lessonId):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	lesson = Lessons.query.get(lessonId)
	form = PostLessonForm()
	majors = Majors.query.all()
	subjects = Subjects.query.all()
	if request.method == 'POST':
		try:
			lesson.lesson_name = form.lesson_name.data
			lesson.lesson_description = form.lesson_description.data
			lesson.subjectId = form.subject.data
			lesson.majorId = form.major.data

			if form.attachment.data:
				attachment_file = save_attachment(form.attachment.data)
				lesson.attachment=attachment_file
			db.session.commit()
			flash('success')
			return redirect("/teacher")
		except:
			flash('error')
			return redirect("/teacher")
	return render_template("teacher/edit_lesson.html",lesson=lesson,subjects=subjects,majors=majors,form=form)


@app.route("/student")
@login_required
def student():
	teachers = User.query.filter_by(user_type="teacher").all()
	lessons = Lessons.query.all()
	majors = Majors.query.all()
	subjects = Subjects.query.all()
	return render_template ("student/student.html",
		subjects=subjects,majors=majors,lessons=lessons,teachers=teachers)

@app.route("/lessons/<int:lessonId>/attachments")
@login_required
def lesson_attachments(lessonId):
	lesson = Lessons.query.get(lessonId)
	return render_template("student/lesson_attachments.html",lesson=lesson)

@app.route("/sort/subjects",methods=['GET','POST'])
@login_required
def sort_lessons():
	teachers = User.query.filter_by(user_type="teacher").all()
	majors = Majors.query.all()
	subjects = Subjects.query.all()

	if request.method == 'POST':
		teacher = request.form.get("teacher")
		subject = request.form.get("subject")
		try:
			teacher = User.query.filter_by(full_name=teacher,user_type="teacher").first()
			subject = Subjects.query.filter_by(subject_name=subject).first()
			lessons = Lessons.query.filter_by(subjectId=subject.id,teacherId=teacher.id).all()
			return render_template ("student/student.html",
				subjects=subjects,majors=majors,lessons=lessons,teachers=teachers)
		except Exception as ex:
			print(ex)
			redirect("/student")

#############################




###### library and homeworks ######
 # <a href="/library" class="btn btn-primary">Kitaphana</a>
 #  <a href="/add_library_book" class="btn btn-outline-primary">Kitap goş</a>
 #  <a href="/homeworks" 

@app.route("/library",methods=['GET','POST'])
def library():
	return "welcome to lib"

@app.route("/add_library_book",methods=['GET','POST'])
@login_required
def add_library_book():
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	return "add book"

@app.route("/homeworks",methods=['GET','POST'])
@login_required
def homeworks():
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	return "Check the homeworks"

###############################





######## admin page functions ########

@app.route("/admin/teachers_list",methods=['GET','POST'])
@login_required
def teachers_list():
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	
	if request.method == 'GET':
		teachers = User.query.filter_by(user_type='teacher').all()
		return render_template("admin/teachers_list.html",teachers=teachers)

	if request.method == 'POST':
		username = request.form.get("username")
		full_name = request.form.get("full_name")
		department = request.form.get("department")
		password = request.form.get("password")
		try:
			user_type = 'teacher'
			user = User(
				username=username,
				full_name=full_name,
				password=password,
				user_type=user_type,
				department=department)
			db.session.add(user)
			db.session.commit()
			flash('Mugallym akaunt doredi!','success')
			return redirect("/admin/teachers_list") 
		except:
			flash('Ýalňyşlyk ýuze çykdy!','danger')
			return redirect("/admin/teachers_list")


@app.route("/admin/students_list",methods=['GET','POST'])
@login_required
def students_list():
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")

	if request.method == 'GET':
		students = User.query.filter_by(user_type='student').all()
		return render_template("admin/students_list.html",students=students)

	if request.method == 'POST':
		full_name = request.form.get("full_name")
		student_id = request.form.get("student_id")
		password = request.form.get("password")
		try:
			user_type = 'student'
			user = User(full_name=full_name,password=password,
				user_type=user_type,student_id=student_id)
			db.session.add(user)
			db.session.commit()
			flash('Talyp akaunt doredi!','success')
			return redirect("/admin/students_list") 
		except:
			flash('Ýalňyşlyk ýuze çykdy!','danger')
			return redirect("/admin/students_list")


@app.route("/admin/majors_list",methods=['GET','POST'])
@login_required
def majors_list():
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	if request.method == 'GET':
		majors = Majors.query.all()
		return render_template("admin/majors_list.html",majors=majors)

	if request.method == 'POST':
		major_name = request.form.get("major_name")
		try:
			major = Majors(major_name=major_name)
			db.session.add(major)
			db.session.commit()
			flash('Ugur doredi!','success')
			return redirect("/admin/majors_list") 
		except:
			flash('Ýalňyşlyk ýuze çykdy!','danger')
			return redirect("/admin/majors_list")

@app.route("/admin/majors_list/delete/<int:major_id>")
def delete_major(major_id):
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	major = Majors.query.get(major_id)
	db.session.delete(major)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/admin/majors_list')

@app.route("/admin/subjects_list",methods=['GET','POST'])
@login_required
def subjects_list():
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	if request.method == 'GET':
		subjects = Subjects.query.all()
		return render_template("admin/subjects_list.html",subjects=subjects)

	if request.method == 'POST':
		subject_name = request.form.get("subject_name")
		try:
			subject = Subjects(subject_name=subject_name)
			db.session.add(subject)
			db.session.commit()
			flash('Sapak doredi!','success')
			return redirect("/admin/subjects_list") 
		except:
			flash('Ýalňyşlyk ýuze çykdy!','danger')
			return redirect("/admin/subjects_list")

@app.route("/admin/subjects_list/delete/<int:subject_id>")
def delete_subject(subject_id):
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	subject = Subjects.query.get(subject_id)
	db.session.delete(subject)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/admin/subjects_list')

#### delete methods ####

@app.route("/admin/students_list/delete/<int:id>")
@login_required
def delete_student(id):
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	student = User.query.get(id)
	db.session.delete(student)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/admin/students_list')

@app.route("/admin/teachers_list/delete/<int:id>")
@login_required
def delete_teacher(id):
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	teacher = User.query.get(id)
	db.session.delete(teacher)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/admin/teachers_list')

##############################################


# #### auth and login routes ####
from flask_login import UserMixin

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
	def __repr__ (self):
		return f"User('{self.username}')"


# @app.route("/dropTable")
# def dropTable():
# 	db.drop_all()
# 	db.create_all()
# 	print('created')
# 	return redirect ("/")

@app.route("/")
def main():
	return render_template ("login/main.html")

@app.route("/login")
def login():
	logout_user()
	return render_template ("login/login.html")

@app.route("/login/student",methods=['GET','POST'])
def student_login():
	if request.method == 'GET':
		if current_user.is_authenticated:
			return redirect("/student")
		return render_template ("login/student_login.html")
	if request.method == 'POST':
		student_id = request.form.get("student_id")
		password = request.form.get("password")
		try:
			user = User.query.filter_by(student_id=student_id).first()
			if user:
				if(user.user_type!="student"):
					flash(f'Login ýalňyşlygy, ulanyjy talyp dal!','danger')
					redirect("/")
				elif(user and user.password==password):
					login_user(user)
					next_page = request.args.get('next')
					return redirect(next_page) if next_page else redirect("/student")
				else:
					raise Exception
			else:
				raise Exception
		except Exception as ex:
			print(ex)
			flash(f'Login ýalňyşlygy, ulanyjy ady ya-da açarsöz ýalnyş!','danger')
	return render_template ("login/student_login.html")

@app.route("/login/teacher",methods=['GET','POST'])
def teacher_login():
	if request.method == 'GET':
		if current_user.is_authenticated:
			return redirect("/teacher")
		return render_template ("login/teacher_login.html")
	if request.method == 'POST':
		username = request.form.get("username")
		password = request.form.get("password")
		try:
			user = User.query.filter_by(username=username).first()
			if user:
				if(user.user_type!="teacher"):
					flash(f'Login ýalňyşlygy, ulanyjy mugallym dal!','danger')
					redirect("/")
				elif(user and user.password==password):
					login_user(user)
					next_page = request.args.get('next')
					return redirect(next_page) if next_page else redirect("/teacher")
				else:
					raise Exception
			else:
				raise Exception
		except Exception as ex:
			print(ex)
			flash(f'Login ýalňyşlygy, ulanyjy ady ya-da açarsöz ýalnyş!','danger')
	return render_template ("login/teacher_login.html")

@app.route("/login/admin",methods=['GET','POST'])
def admin_login():
	if request.method == 'GET':
		if current_user.is_authenticated:
			return redirect("/admin/teachers_list")
		return render_template ("login/admin_login.html")
	if request.method == 'POST':
		username = request.form.get("username")
		password = request.form.get("password")
		try:
			user = User.query.filter_by(username=username).first()
			if user:
				if(user.user_type!="admin"):
					flash(f'Login ýalňyşlygy, ulanyjy admin dal!','danger')
					redirect("/")
				if(user and user.password==password):
					login_user(user)
					next_page = request.args.get('next')
					return redirect(next_page) if next_page else redirect("/admin/teachers_list")
				else:
					raise Exception
			else:
				raise Exception				
		except Exception as ex:
			flash(f'Login ýalňyşlygy, ulanyjy ady ya-da açarsöz ýalnyş!','danger')
			print(ex)
	return render_template ("login/admin_login.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect ("/")

#  #### end of login routes ####


### forms ###
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,ValidationError
# from routes import Lessons,Majors,Subjects,Users

def getMajors():
	majorsList=[]
	majors = Majors.query.all()
	for major in majors:
		obj=(major.id,major.major_name)
		majorsList.append(obj)
	return majorsList

def getSubjects():
	subjectsList=[]
	subjects = Subjects.query.all()
	for subject in subjects:
		obj=(subject.id,subject.subject_name)
		subjectsList.append(obj)
	return subjectsList

def getAttachments(lessonId):
	attachmentsList=[]
	lessons = Lessons.query.get(lessonId)
	for attachment in lessons.attachments:
		obj=(attachment.id,attachment.filename)
		attachmentsList.append(obj)
	return attachmentsList
# usersList=[]
# for profile in User:
# 	usersList.append(profile)

class UploadFileForm(FlaskForm):
	file = FileField('Faýl ýükläň')
	submit = SubmitField('Ýükle')

class PostLessonForm(FlaskForm):
	lesson_name = StringField('Temanyň ady:',validators=[DataRequired()])
	lesson_description = StringField('Beýany:')
	subject = SelectField('Dersiň ady:',choices=getSubjects(),validators=[DataRequired()])
	major = SelectField('Ugry:',choices=getMajors(),validators=[DataRequired()])
	# teacher = StringField('Ugry:',choices=majorsList,validators=[DataRequired()])
	attachment = FileField('Sapak ýükläň:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Ýükle')

class AddAttachmentForm(FlaskForm):
	filename = StringField('Faýlyň ady:',validators=[DataRequired()])
	attachment = FileField('Faýl:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Ýükle')

class PostReferenceForm(FlaskForm):
	reference_name = StringField('Temanyň ady:',validators=[DataRequired()])
	subject = SelectField('Dersiň ady:',choices=getSubjects(),validators=[DataRequired()])
	major = SelectField('Ugry:',choices=getMajors(),validators=[DataRequired()])
	# teacher = StringField('Ugry:',choices=majorsList,validators=[DataRequired()])
	attachment = FileField('Sapak ýükläň:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Ýükle')
########

if __name__ == "__main__":
	app.run(host="0.0.0.0" , port=5000 , debug=True)