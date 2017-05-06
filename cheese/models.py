from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

# [START model]

class User(db.Model):
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)
    first_name = db.Column(db.UnicodeText())
    last_name = db.Column(db.UnicodeText())
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.UnicodeText())
    pw_hash = db.Column(db.UnicodeText())
    timekit_token = db.Column(db.UnicodeText())

# [END model]

def _create_database():
    '''
    If this script is run directly, create all the tables necessary to run the
    application.
    '''
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
        SQLALCHEMY_DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')
        print('All tables created')

if __name__ == '__main__':
    _create_database()
