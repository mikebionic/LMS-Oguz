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
'''
class University(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	university_name = db.Column(db.String(100),nullable=False)
	university_description = db.Column(db.String())
	logo = db.Column(db.String(500))
	faculties = db.relationship('Faculty',backref='university',lazy='joined')

'''
class Faculty(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	faculty_name = db.Column(db.String(100),nullable=False)
	faculty_description = db.Column(db.String(500))
	icon = db.Column(db.String(100))
	universityId = db.Column(db.Integer,db.ForeignKey("university.id"))
### Lesson models ###

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


# #### auth and login routes ####
from flask_login import UserMixin


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

db.drop_all()
db.create_all()

# Required admin user

admin = User(username="administrator",password="lms_system@root/key:nc326y9nrivf3rrpvlbjHVKCRDESWTAQ!2344IGJ(BpPM<>?><0UB)C3bn4ic0i-MNBVCX:{;>#>%>)cx[]",
	user_type="admin",full_name="Administrator")
db.session.add(admin)

'''

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


university = University(university_name="Türkmenistanyň Oguz han adyndaky inžener-tehnologiýalar uniwersiteti",
	university_description="Türkmenistanyň Oguz han adyndaky inžener-tehnologiýalar uniwersiteti Ýaponiýanyň Sukuba uniwersiteti bilen hyzmatdaşlygy giňeldýär. Bilim, ylym we tehnologiýalar ulgamynda halkara hyzmatdaşlygyny giňeltmek meselesi Türkmenistanyň hökümet mejlisinde ara alnyp maslahatlaşyldy. Şu okuw ýylynda ýurdumyz üçin täze ugurlar boýunça hünärmenleri taýýarlamak maksady bilen Ýaponiýanyň bu ýokary okuw mekdebinden ýene-de birnäçe professorlary we mugallymlary çagyrmak meýilleşdirilýär.",
	logo="ulogo.png")
db.session.add(university)

db.session.commit()

faculty = Faculty(faculty_name="Dil öwreniş bölümi",
	faculty_description="Uniwersitetde iňlis we ýapon dillerini öwrenmek üçin ähli şertler döredilendir. Lingofon otaglary, görkezme esbaplary, daşary ýurt dillerindäki kitaplar, okuw gollanmalary, ýokary derejeli professor-mugallymlar hemişe talyplaryň hyzmatyndadyr.",
	icon=None,universityId=1)
db.session.add(faculty)

faculty = Faculty(faculty_name="Innowasiýalaryň ykdysadyýeti",
	faculty_description="Bu fakultet “ykdysadyýet we innowasiýa” pudaklarynda işleýän, innowasion jemgyýeti döretmäge bäsleşige ukyply alymlary, tehniki bilermenleri, işewürleri, ykdysadyýetçileri, menejerleri, marketologlary taýýarlar.",
	icon=None,universityId=1)
db.session.add(faculty)

faculty = Faculty(faculty_name="Biotehnologiýa we ekologiýa",
	faculty_description="Häzirki wagtda uniwersitetiň Biotehnologiýa we ekologiýa fakultetinde biotehnologiýa, ekologiýa we tebigatdan peýdalanmak, öýjük we molekulýar biologiýa hem-de genetika we bioinžiniring ýaly dünýäde ileri tutulýan ugurlar boýunça ýokary bilimli hünärmenler taýýarlanylýar.",
	icon=None,universityId=1)
db.session.add(faculty)

faculty = Faculty(faculty_name="Awtomatika we elektronika",
	faculty_description="Häzirkizaman jemgyýetinde robotlar diňe bir önümçilikde däl, eýsem durmuş we öý şertlerinde hem giňden ulanylýar. Robotlar adamyň keselini bejermekden başlap, älemi öwrenmek pudaklaryna çenli durmuşyň ähli ýerlerinde ulanylýar. Ýakyn gelejekde robotlar ýönekeý serişde bolman, eýsem olar adam jemgyýetiniň aýrylmaz bölegi bolar.",
	icon=None,universityId=1)
db.session.add(faculty)

faculty = Faculty(faculty_name="Himiki we nanotehnologiýa",
	faculty_description="Energiýa we materiallar ýaşaýşyň we siwilizasiýalaryň, ylmyň we tehnikanyň ösüşiniň hereketlendiriji güýjüdir. Olar senagatyň dürli pudaklarynyň we ulag-aragatnaşyk ulgamynyň ösmeginde, maglumatlary ýygnamak, seljermek, başga ýerlere geçirmek, ähli tehnologiýalary döretmek we dolandyrmak üçin zerur bolan elektronikanyň kämilleşmeginde, şeýle-de ýaşaýşyň derejesini ýokarlandyrmak üçin zerur bolan enjamlaryň önümçiliginde innowasiýalaryň çeşmesi bolup hyzmat edýär.",
	icon=None,universityId=1)
db.session.add(faculty)

faculty = Faculty(faculty_name="Kompýuter ylymlary we maglumat tehnologiýalary",
	faculty_description="Maglumat ulgamlary we tehnologiýalary, Informatika we hasaplaýyş tehnikasy, Animasiýa we grafika dizaýny, Sanly ykdysadyýet, Mobil we tor inžiniringi, Sanly infrastruktura we kiberhowpsuzlyk, Amaly matematika we informatika ýaly dünýäde ileri tutulýan ugurlar boýunça ýokary bilimli hünärmenler taýýarlanylýar.",
	icon=None,universityId=1)
db.session.add(faculty)

'''

db.session.commit()