class Config:
	FLASK_ENV = 'development'
	TESTING = True
	SECRET_KEY = "sasdfkknronf43nf03p4fn0u3b5npf"

	# Database
	SQLALCHEMY_DATABASE_URI = "sqlite:///lms.db"
	UPLOAD_FOLDER = "static/post_uploads"