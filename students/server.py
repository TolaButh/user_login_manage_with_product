from enum import unique
from flask import Flask,render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.utils import redirect
import os, secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SECRET_KEY']=b'tola1221'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

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
@app.route("/")
def home():
    title = "Home Page"
    return render_template('index.html',title=title)

@app.route("/faculties")
def faculties():
    faculties = Faculty.query.all()
    return render_template('faculties.html',title="Faculties",faculties=faculties)
@app.route("/add_faculty",methods=['POST', 'GET'])
def add_faculty():
    if request.method == "POST":
        faculty_name = request.form['faculty_name']
        faculty = Faculty(faculty_name= faculty_name)
        db.session.add(faculty)
        db.session.commit()
        return redirect(url_for('faculties'))
    return render_template('add_faculty.html',title="New faculty")
@app.route("/update_faculty<int:id>",methods=['POST', 'GET'])
def update_faculty(id):
    faculty = Faculty.query.filter_by(id=id).first()
    if request.method == "POST":
        faculty.faculty_name = request.form['faculty_name']
        db.session.commit()
        return redirect(url_for('faculties'))
    return render_template('update_faculty.html',title="Update faculty",faculty=faculty)
@app.route("/students")
def students():
    students = Student.query.all()
    return render_template('students.html',title="Show Student", students= students)


@app.route("/add_student",methods=['POST', 'GET'])
def add_student():
    faculty= Faculty.query.all()
    if request.method == "POST":
        student_id =request.form['student_id']
        student_name=request.form['student_name']
        faculty_id = request.form['faculty_id']
        student = Student(student_id=student_id, student_name= student_name,faculty_id=faculty_id)
        
        db.session.add(students)
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('add_student.html',title="New Student",faculty=faculty)

def save_image(img):
    random_hex = secrets.token_hex(8)
    fn, fext = os.path.splitext(img.filename)
    img_fn = random_hex + fext
    img_path = os.path.join(app.root_path, 'static/images'.image_fn)
    img.save(img_path)
    return img_fn

@app.route("/student/update/<int:id>",methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get(id)
    faculties = Faculty.query.all()
    if request.method== 'POST':
        student_name= request.form['student_name']
        faculty_id = request.form['faculty_id']
        student_img = request.files['student_img']
        faculty = Faculty.query.get(faculty_id)
        student = Student.query.get(id)
        if student_img:
            pic_file = save_image(student_img)
            student.student_img =pic_file
        student.student_name=student_name
        student.faculty = faculty
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))    
    return render_template('update_student.html',title="Update Student", faculties = faculties ,student = student)


if __name__ == "__main__":
    app.run(debug=True)

