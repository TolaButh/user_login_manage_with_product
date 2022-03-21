from flaskstudent import db,login_manager
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.String(11), nullable=False, unique=True)
    student_name = db.Column(db.String(50),nullable=False)
    student_img = db.Column(db.String(50),nullable=False, default='default.png')
    faculty_id = db.Column(db.Integer(), db.ForeignKey('faculty.id'))
    def __repr__(self):
        return '<Student: {} >'.format(self.student_name)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_name = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', backref='faculty', lazy='dynamic')
    def __repr__(self):
        return f'faculty: {self.faculty_name}'
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<User: {}>'.format(self.username)
    