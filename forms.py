from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,ValidationError

class PostLessonForm(FlaskForm):
	lesson_theme = StringField('Temanyň ady:',validators=[DataRequired()])
	subject = StringField('Dersiň ady:',validators=[DataRequired()])
	major = StringField('Ugry:',validators=[DataRequired()])
	attachment = FileField('Sapak yuklaň:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Yukle')

class UploadFileForm(FlaskForm):
	file = FileField('Upload File')
	submit = SubmitField('Upload')