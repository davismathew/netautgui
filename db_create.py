#!flask/bin/python
from migrate.versioning import api
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
db.create_all()
