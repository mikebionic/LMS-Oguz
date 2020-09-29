from flask import (Flask,
									render_template,
									url_for,
									flash,
									redirect,
									request,
									Response,
									abort)
from main import app
from main import db
from flask_login import (login_user,
												current_user,
												logout_user,
												login_required)

from .models import (User,
										Lessons,
										Majors,
										Subjects,
										Attachments)

from .forms import (PostLessonForm,
									AddAttachmentForm)
from .utils import save_attachment


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


@app.route("/teacher",methods=['GET','POST'])
@login_required
def teacher():
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	form = PostLessonForm()
	form.major.choices = getMajors()
	form.subject.choices = getSubjects()

	majors = Majors.query.all()
	subjects = Subjects.query.all()

	if request.method == 'GET':
		try:
			lessons = Lessons.query.filter_by(teacherId=current_user.id)
		except:
			lessons = Lessons.query.order_by(Lessons.date_added).all()
		majors = Majors.query.all()
		subjects = Subjects.query.all()
		return render_template ("teacher/teacher.html",title="Sapagy ýükle",
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
	return render_template ("teacher/teacher.html",title="Sapagy ýükle",subjects=subjects,majors=majors,form=form)


@app.route("/lessons/attach/<int:lessonId>",methods=['GET','POST'])
@login_required
def attach(lessonId):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	lesson = Lessons.query.get(lessonId)
	form = AddAttachmentForm()
	if request.method == 'POST':
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
	return render_template("teacher/add_attachment.html",title="Faýl goş",lesson=lesson,form=form)


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
	form.major.choices = getMajors()
	form.subject.choices = getSubjects()

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
	return render_template("teacher/edit_lesson.html",title="Sapagy üýtget",lesson=lesson,subjects=subjects,majors=majors,form=form)


@app.route("/student")
@login_required
def student():
	teachers = User.query.filter_by(user_type="teacher").all()
	lessons = Lessons.query.order_by(Lessons.date_added).all()
	majors = Majors.query.all()
	subjects = Subjects.query.all()
	return render_template ("student/student.html",title="Sapak ýüklemek",
		subjects=subjects,majors=majors,lessons=lessons,teachers=teachers)


@app.route("/lessons/<int:lessonId>/attachments")
@login_required
def lesson_attachments(lessonId):
	lesson = Lessons.query.get(lessonId)
	return render_template("student/lesson_attachments.html",title="Faýllar",lesson=lesson)


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
			return render_template ("student/student.html",title="Sapak ýüklemek",
				subjects=subjects,majors=majors,lessons=lessons,teachers=teachers)
		except Exception as ex:
			print(ex)
			redirect("/student")

#############################


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

# @app.route("/dropTable")
# def dropTable():
# 	db.drop_all()
# 	db.create_all()
# 	print('created')
# 	return redirect ("/")

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