from flask import (render_template,
									url_for,
									flash,
									redirect,
									request,
									Response,
									abort)
from flask_login import login_user,current_user,logout_user,login_required

from main import app
from main import db

from .forms import PostReferenceForm
from .routes_lms import getMajors,getMajors
from .models import Majors,Lessons,Reference
from .utils import save_attachment

@app.route('/')
@app.route('/main')
def home_page():
	return render_template('library/index.html')

@app.route('/projects')
def projects_page():
	return render_template('library/projects.html')

@app.route('/tutorials')
def tutorials_page():
	return render_template('library/tutorials.html')

@app.route('/list')
def lists_page():
	return render_template('library/list.html')

@app.route("/library",methods=['GET','POST'])
def library():
	majors = Majors.query.all()
	references = Reference.query.all()
	return render_template('library/library.html',
		references=references,majors=majors)

@app.route("/add_library_book",methods=['GET','POST'])
@login_required
def add_library_book():
	if(current_user.user_type!="teacher"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/")
	form = PostReferenceForm()
	form.major.choices = getMajors()

	majors = Majors.query.all()

	if request.method == 'GET':
		try:
			references = Reference.query.filter_by(teacherId=current_user.id)
		except:
			references = Reference.query.all()
		majors = Majors.query.all()
		return render_template ("library/add_library_book.html",
			references=references,majors=majors,form=form)
	if request.method == 'POST':
		reference = {
			'reference_name':form.reference_name.data,
			'reference_description':form.reference_description.data,
			'majorId':form.major.data,
			'teacherId':current_user.id
		}
		if form.attachment.data:
			attachment_file = save_attachment(form.attachment.data)
			reference.update({'attachment':attachment_file})

		newReference = Reference(**reference)
		db.session.add(newReference)
		db.session.commit()
		flash('Reference successfully added', 'success')
		return redirect('/add_library_book')
	return render_template ("library/add_library_book.html",
		majors=majors,form=form)