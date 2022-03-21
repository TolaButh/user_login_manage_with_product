from flask_login.utils import login_required
from flaskstudent import app,db,bcrypt, login_manager
from flask import redirect, render_template,request,flash,url_for
import os, secrets
from flaskstudent.models import Student, Faculty, User
from flask_login import login_user,logout_user
from flask_login import login_required
@app.route("/", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
   
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route("/loyout")
def loyout():
    logout_user()
    return redirect(url_for('login'))
@app.route("/home")
@login_required
def home():
    title = "Home Page"
    return render_template('index.html',title=title)

@app.route("/faculties")
@login_required
def faculties():
    faculties = Faculty.query.all()
    return render_template('faculties.html',title="Faculties",faculties=faculties)
@app.route("/add_faculty",methods=['POST', 'GET'])
@login_required
def add_faculty():
    if request.method == "POST":
        faculty_name = request.form['faculty_name']
        faculty = Faculty(faculty_name= faculty_name)
        db.session.add(faculty)
        db.session.commit()
        flash('Add Faculty Successfully!', 'success')
        return redirect(url_for('faculties'))
    return render_template('add_faculty.html',title="New faculty")

@app.route("/update_faculty<int:id>",methods=['POST', 'GET'])
@login_required
def update_faculty(id):
    faculty = Faculty.query.filter_by(id=id).first()
    if request.method == "POST":
        faculty.faculty_name = request.form['faculty_name']
        db.session.commit()
        flash('Update Faculty Successfully!', 'success')
        return redirect(url_for('faculties'))
    return render_template('update_faculty.html',title="Update faculty",faculty=faculty)
@app.route("/students")
@login_required
def students():
    students = Student.query.all()
    return render_template('students.html',title="Show Student", students= students)


@app.route("/add_student",methods=['POST', 'GET'])
@login_required
def add_student():
    faculties= Faculty.query.all()
    if request.method == "POST":
        student_id =request.form['student_id']
        student_name=request.form['student_name']
        faculty_id = request.form['faculty_id']
        students = Student(student_id=student_id, student_name= student_name,faculty_id=faculty_id)
        
        db.session.add(students)
        db.session.commit()
        flash('Add Student Successfully!', 'success')
        return redirect(url_for('students'))
    return render_template('add_student.html',title="New Student",faculties=faculties)
@app.route("/delete_student<int:id>")
@login_required
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('student')
def save_image(img):
    random_hex = secrets.token_hex(8)
    fn, fext = os.path.splitext(img.filename)
    img_fn = random_hex + fext
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_fn)
    img.save(img_path)
    return img_fn

@app.route("/student/update/<int:id>",methods=['GET', 'POST'])
@login_required
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
        flash('Update Student Successfully!', 'success')
        return redirect(url_for('students'))    
    return render_template('update_student.html',title="Update Student", faculties = faculties ,student = student)

