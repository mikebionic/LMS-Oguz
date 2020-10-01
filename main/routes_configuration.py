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

from .forms import UniversityForm
from .models import University, Faculty
from .utils import save_attachment


@app.route('/admin/university_config', methods=['GET','POST'])
def university_config():
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/")
	form = UniversityForm()
	university = University.query.get(1)
	
	if request.method == 'POST':
		university.university_name = form.university_name.data
		university.university_description = form.university_description.data

		if form.logo.data:
			attachment_file = save_attachment(form.logo.data)
			university.logo = attachment_file

		db.session.commit()
		flash('university successfully updated', 'success')
		return redirect('/admin/university_config')

	form.university_name.data = university.university_name
	form.university_description.data = university.university_description
	return render_template ("admin/university_config.html",
		university=university,form=form)


@app.route("/admin/faculties",methods=['POST'])
@login_required
def faculties():
	if(current_user.user_type!="admin"):
		flash('Siz shu penjira girip bilenzok!')
		return redirect("/login")

	if request.method == 'POST':
		faculty_name = request.form.get("faculty_name")
		faculty_description = request.form.get("faculty_description")
		icon = request.form.get("icon")
		university = University.query.get(1)
		try:
			faculty = Faculty(
				faculty_name = faculty_name,
				faculty_description = faculty_description,
				icon = icon,
				universityId = university.id)
			db.session.add(faculty)
			db.session.commit()
			return redirect("/admin/university_config") 
		except:
			return redirect("/admin/university_config")