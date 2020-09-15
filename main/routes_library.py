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

@app.route('/')
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
	return render_template('library/library.html')

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