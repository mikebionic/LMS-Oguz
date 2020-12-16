from main import app
import os,secrets
from PIL import Image
from werkzeug.utils import secure_filename
from importlib import import_module
from datetime import date,datetime,time
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'])

def save_attachment(form_attachment):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_attachment.filename)
	attachment_fn = random_hex + f_ext
	attachment_path = os.path.join(app.root_path, 'static/attachments/', attachment_fn)
	print('attachment_path')
	form_attachment.save(attachment_path)
	print('saved')
	return attachment_fn