from flask import Flask,render_template,url_for,flash,redirect,request,Response,abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from forms import PostLessonForm,UploadFileForm

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lessonsShare.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'main'
login_manager.login_message = 'Programma girin!'
login_manager.login_message_category = 'info'



# #### lessons db and CRUD #####

class Lessons(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	lesson_theme = db.Column(db.String(100),nullable =False)
	subject = db.Column(db.String(100))
	major = db.Column(db.String(100))
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	attachment = db.Column(db.String(500))
	teacherId = db.Column(db.Integer)

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
	form = PostLessonForm()
	if request.method == 'GET':
		lessons = Lessons.query.all()
		return render_template ("teacher/teacher.html",lessons=lessons,form=form)
	if request.method == 'POST':
		print('post request')
		if form.validate_on_submit():
			lesson = {
				'lesson_theme':form.lesson_theme.data,
				'subject':form.subject.data,
				'major':form.major.data,
				'teacherId':current_user.id
			}
			print(lesson)
			if form.attachment.data:
				attachment_file = save_attachment(form.attachment.data)
				lesson.update({'attachment':attachment_file})
			print(lesson)
			newLesson = Lessons(**lesson)
			db.session.add(newLesson)
			db.session.commit()
			print('lesson success')
			flash('Lesson successfully added', 'success')
			redirect('/teacher')
	return render_template ("teacher/teacher.html",form=form)

@app.route("/student")
def student():
	lessons = Lessons.query.all()
	return render_template ("student/student.html",lessons=lessons,form=form)

#############################




# #### auth and login routes ####
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(50),unique=True,nullable =False)
	full_name = db.Column(db.String(100))
	password = db.Column(db.String(100), nullable=False)
	user_type = db.Column(db.String(100))
	def __repr__ (self):
		return f"User('{self.username}')"


@app.route("/dropTable")
def dropTable():
	db.drop_all()
	db.create_all()
	print('created')
	return redirect ("/")

@app.route("/")
@app.route("/main")
def main():
	return render_template ("login/main.html")

@app.route("/login/student",methods=['GET','POST'])
def student_login():
	if request.method == 'GET':
		if current_user.is_authenticated:
			return redirect("/student")
		return render_template ("login/student_login.html")
	if request.method == 'POST':
		username = request.form.get("username")
		password = request.form.get("password")
		try:
			user = User.query.filter_by(username=username).first()
			if user:
				if(user.user_type!="student"):
					redirect("/")
				if(user and user.password==password):
					login_user(user)
					next_page = request.args.get('next')
					return redirect(next_page) if next_page else redirect("/student")
				else:
					flash(f'Login ýalňyşlygy, ulanyjy ady ya-da açarsöz ýalnyş!','danger')
			else:
				flash(f'Login ýalňyşlygy, ulanyjy talyp dal!','danger')
		except ValueError as ex:
			print(ex)
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
					redirect("/")
				if(user and user.password==password):
					login_user(user)
					next_page = request.args.get('next')
					return redirect(next_page) if next_page else redirect("/teacher")
				else:
					flash(f'Login ýalňyşlygy, ulanyjy ady ya-da açarsöz ýalnyş!','danger')
			else:
				flash(f'Login ýalňyşlygy, ulanyjy mugallym dal!','danger')
		except ValueError as ex:
			print(ex)
	return render_template ("login/teacher_login.html")

@app.route("/login/admin")
def admin_login():
	return render_template ("login/admin_login.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect ("/")

@app.route("/register",methods=['GET','POST'])
def register():
	if request.method == 'GET':
		if current_user.is_authenticated:
			return redirect("/student")
		return render_template ("login/register.html")
	if request.method == 'POST':
		if request.form:
			username = request.form.get("username")
			password = request.form.get("password")
			full_name = request.form.get("full_name")
			if full_name==None:
				full_name=''
			user_type = request.form.get('user_type')
			try:
				user = User(username=username,password=password,
					full_name=full_name,user_type=user_type)
				print(user)
				print('success')
				db.session.add(user)
				db.session.commit()
				flash('Ulanyjy akaunt doredi!','success')
				return redirect("/") 
			except ValueError as ex:
				print(ex)
			else:
				flash('Açarsözler deň däl!','warning')
		return render_template ("login/register.html")

#  #### end of login routes ####


if __name__ == "__main__":
	app.run(host="0.0.0.0" , port=5000 , debug=True)