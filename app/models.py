from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

members = db.Table('members',
                   db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                   db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
                   )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    fullname = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if self.password is not None:
            return check_password_hash(self.password, password)
        else:
            return None

    def __init__(self, username, email, password, fullname=None, active=True):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.active = active
        self.created = datetime.now()
        self.set_password(password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', secondary=members, lazy='subquery', backref=db.backref('groups', lazy=True))
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, name):
        self.name = name
        self.created = datetime.now()

    def __repr__(self):
        return '<Group: {}>'.format(self.name)


class License(db.Model):
    __tablename__ = 'licenses'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255))
    key = db.Column(db.String(255))
    user = db.Column(db.Integer)
    group = db.Column(db.Integer)
    expire = db.Column(db.Date)
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)

    def __init__(self, product, key, user, group=None, expire=None, email=None, active=True):
        self.product = product
        self.key = key
        self.user = user
        self.group = group
        self.expire = expire
        self.email = email
        self.active = active
        self.created = datetime.now()
        self.updated = datetime.now()

    def __repr__(self):
        return '<License: {}>'.format(self.product)
