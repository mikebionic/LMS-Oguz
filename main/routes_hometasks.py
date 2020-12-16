from flask import (
	render_template,
	url_for,
	flash,
	redirect,
	request,
	Response,
	abort)
from flask_login import login_user,current_user,logout_user,login_required

from main import app
from main import db

from .forms import PostHometaskForm,PostSolutionForm
from .routes_lms import getMajors,getSubjects
from .models import Majors,Subjects,Lessons,Hometask,Solution,User
from .utils import save_attachment


@app.route("/manage_hometasks",methods=['GET','POST'])
@login_required
def manage_hometasks():
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/")
	form = PostHometaskForm()
	form.major.choices = getMajors()
	form.subject.choices = getSubjects()

	majors = Majors.query.all()
	subjects = Subjects.query.all()

	if request.method == 'GET':
		hometasks = Hometask.query.filter_by(teacherId=current_user.id).order_by(Hometask.date_added).all()
		majors = Majors.query.all()
		subjects = Subjects.query.all()
		return render_template ("teacher/manage_hometasks.html",title="Öý işleri ýüklemek",
			hometasks=hometasks,majors=majors,subjects=subjects,form=form)
	
	if request.method == 'POST':
		hometask = {
			'hometask_name':form.hometask_name.data,
			'hometask_description':form.hometask_description.data,
			'majorId':form.major.data,
			'subjectId':form.subject.data,
			'teacherId':current_user.id
		}
		if form.attachment.data:
			attachment_file = save_attachment(form.attachment.data)
			hometask.update({'attachment':attachment_file})

		newHometask = Hometask(**hometask)
		db.session.add(newHometask)
		db.session.commit()
		flash('Hometask successfully added', 'success')
		return redirect('/manage_hometasks')
	return render_template ("teacher/manage_hometasks.html",title="Öý işleri ýüklemek",
		majors=majors,subjects=subjects,form=form)


@app.route("/hometasks/<hometaskId>/solutions",methods=['GET','POST'])
@login_required
def solutions(hometaskId):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/")
	if request.method == 'GET':
		hometask = Hometask.query.filter_by(id=hometaskId).first()
		solutions = Solution.query.filter_by(hometaskId=hometask.id).order_by(Solution.date_added).all()
		majors = Majors.query.all()
		subjects = Subjects.query.all()
		students = User.query.filter_by(user_type="student").all()
		return render_template ("teacher/solutions.html",title="Çözülüşler",
			solutions=solutions,hometask=hometask,
			students=students,majors=majors,subjects=subjects)

@app.route("/hometasks")
@login_required
def hometasks():
	hometasks = Hometask.query.order_by(Hometask.date_added).all()
	majors = Majors.query.all()
	subjects = Subjects.query.all()
	teachers = User.query.filter_by(user_type="teacher").all()
	return render_template ("student/hometasks.html",title="Öý işler",
		hometasks=hometasks,majors=majors,subjects=subjects,teachers=teachers)


@app.route("/hometasks/delete/<int:hometaskId>",methods=['GET'])
@login_required
def delete_hometask(hometaskId):
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")
	hometask = Hometasks.query.get(hometaskId)
	db.session.delete(hometask)
	db.session.commit()
	flash('successfully deleted!')
	return redirect('/teacher')


@app.route("/hometasks/<hometaskId>/post_solution",methods=['GET','POST'])
@login_required
def post_solution(hometaskId):
	if(current_user.user_type!="student"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/")
	form = PostSolutionForm()
	if request.method == 'GET':
		hometask = Hometask.query.filter_by(id=hometaskId).first()
		solutions = Solution.query.filter_by(studentId=current_user.id).order_by(Solution.date_added).all()
		majors = Majors.query.all()
		subjects = Subjects.query.all()
		return render_template ("student/post_solution.html",title="Çözülişi ýüklemek",
			hometasks=hometasks,solutions=solutions,majors=majors,subjects=subjects,form=form)
	
	if request.method == 'POST':
		solution = {
			'solution_name':form.solution_name.data,
			'solution_description':form.solution_description.data,
			'completed':form.completed.data,
			'hometaskId':hometaskId,
			'studentId':current_user.id
		}
		if form.attachment.data:
			attachment_file = save_attachment(form.attachment.data)
			solution.update({'attachment':attachment_file})

		newSolution = Solution(**solution)
		db.session.add(newSolution)
		db.session.commit()
		flash('Solution successfully added', 'success')
		return redirect('/hometasks')
	return render_template ("student/post_solution.html",title="Çözülişi ýüklemek",
		hometask=hometask,majors=majors,subjects=subjects,form=form)


@app.route("/sort/hometasks",methods=['GET','POST'])
@login_required
def sort_hometasks():
	hometasks = Hometask.query.order_by(Hometask.date_added).all()
	majors = Majors.query.all()
	subjects = Subjects.query.all()
	teachers = User.query.filter_by(user_type="teacher").all()
	
	if request.method == 'POST':
		teacher = request.form.get("teacher")
		subject = request.form.get("subject")

		try:
			teacher = User.query.filter_by(full_name=teacher,user_type="teacher").first()
			subject = Subjects.query.filter_by(subject_name=subject).first()
			hometasks = Hometask.query.filter_by(subjectId=subject.id,teacherId=teacher.id).all()

			return render_template ("student/hometasks.html",title="Öý işler",
				hometasks=hometasks,majors=majors,subjects=subjects,teachers=teachers)

		except Exception as ex:
			print(ex)
			redirect("/student")
