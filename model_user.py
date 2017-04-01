from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

database_url = 'mysql://%s:%s@%s:%s/%s' % ("root", "123456", "localhost", 3306, "flask_test")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    stream_key = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(15), unique=True)
    is_up = db.Column(db.Boolean, nullable=False)
    avatar_path = db.Column(db.String(50))

    def __init__(self, id, name, password, stream_key, phone, avatar_path):
        self.id = id
        self.name = name
        self.password = password
        self.stream_key = stream_key
        self.phone = phone
        self.is_up = is_up
        self.avatar_path = avatar_path
    
    def __repr__(self):
        return '' % (self.id, self.name)

class Stream(db.Model):
    stream_key = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(50))
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, stream_key, title, level):
        self.stream_key = stream_key
        self.title = title
        self.level = level

    def __repr__(self):
        return '' % (self.stream_key, self.title)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    from_user_id = db.Column(db.Integer, nullable=False)
    to_user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, id, from_user_id, to_user_id):
        self.id = id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id

    def __repr__(self):
        return '' % (self.from_user_id, self.to_user_id)

class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value

    def __repr__(self):
        return '' % (self.name, self.value)

db.create_all()