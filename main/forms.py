from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,ValidationError


class UploadFileForm(FlaskForm):
	file = FileField('Faýl ýükläň')
	submit = SubmitField('Ýükle')


class PostLessonForm(FlaskForm):
	lesson_name = StringField('Temanyň ady:',validators=[DataRequired()])
	lesson_description = StringField('Beýany:')
	subject = SelectField('Dersiň ady:',coerce=int,validators=[DataRequired()])
	major = SelectField('Ugry:',coerce=int,validators=[DataRequired()])
	attachment = FileField('Sapak ýükläň:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Ýükle')


class AddAttachmentForm(FlaskForm):
	filename = StringField('Faýlyň ady:',validators=[DataRequired()])
	attachment = FileField('Faýl:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Ýükle')


class PostReferenceForm(FlaskForm):
	reference_name = StringField('Kitabyň ady:',validators=[DataRequired()])
	reference_description = StringField('Beýany:')
	major = SelectField('Ugruň ady:',coerce=int,validators=[DataRequired()])
	attachment = FileField('Sapak ýükläň:',validators=[FileAllowed(
		['mp4','mov','3gp','webm','jpg','jpeg','doc','docx','txt','odt','pdf','djvu'])])
	submit = SubmitField('Ýükle')