import os

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_dir = os.path.join(basedir, 'uploads')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SwC@z4m23i2dkmd^bZN@Yw'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 1
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads')
