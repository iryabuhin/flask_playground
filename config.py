import os

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_dir = os.path.join(basedir, 'uploads')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TASKS_PER_PAGE = 4
    UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads')
    UPLOADED_FILES_ALLOW = []
