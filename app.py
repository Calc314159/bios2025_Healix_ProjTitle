from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdatabase.db'
db = SQLAlchemy(app)
app.secret_key = 'GhfhLJasdFdkfShjLdf'

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    yearlevel = db.Column(db.String(100), nullable = False)
    capacity = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now())

    students = db.relationship('Student', backref = "classroom")
    teachers = db.relationship('Teacher', backref = "classroom")

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100), nullable = False)
    lastname = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now())
    bio = db.Column(db.Text)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now())
    bio = db.Column(db.Text)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.name}>'

app.app_context().push()
db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return render_template("hello.html")

@app.route("/shapes")
def shapes():
    return render_template("shapes.html")

@app.route("/variables")
def variables():
    my_data = "x=(-b+-\sqrt(b^2-4ac) )/2a"
    return render_template("variables.html", data=my_data)

@app.route("/conditionals")
def conditionals():
    score = 100
    return render_template("conditionals.html", score=score)

@app.route("/loops")
def loops():
    mylist=["3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679",2.718281828459045,"golden ratio",78,97.49]
    return render_template("loops.html", itemlist=mylist)

@app.route("/viewclassrooms")
def viewclassrooms():
    classrooms = Classroom.query.all()
    return render_template("viewclassrooms.html",classrooms=classrooms)

@app.route("/create", methods=["get","post"])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        yearlevel = request.form['yearlevel']
        capacity = request.form['capacity']
        classroom=Classroom(name=name,yearlevel=yearlevel,capacity=capacity)
        db.session.add(classroom)
        db.session.commit()
        return redirect(url_for("viewclassrooms"))

    return render_template("create.html")

@app.route("/<int:classroom_id>/studentcreate", methods=('GET', 'POST'))
@login_required
def studentcreate(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname, lastname=lastname, email=email, age=age, bio=bio, classroom_id=classroom_id)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("viewclassrooms"))
  
    return render_template("studentcreate.html",classroom = classroom)

@app.route("/<int:classroom_id>/teachercreate", methods=('GET', 'POST'))
@login_required
def teachercreate(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        teacher = Teacher(name=name, email=email, age=age, bio=bio, classroom_id=classroom_id)
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for("viewclassrooms"))
  
    return render_template("teachercreate.html",classroom = classroom)

@app.route("/studentedit/<int:student_id>", methods=('GET', 'POST', 'PUT'))
@login_required
def studentedit2(student_id):
    if request.method == 'POST':
        student = Student.query.get(student_id)
        
        firstname2 = request.form['firstname']
        lastname2 = request.form['lastname']
        email2 = request.form['email']
        age2 = int(request.form['age'])
        bio2 = request.form['bio']

        student.firstname = firstname2
        student.lastname = lastname2
        student.email = email2
        student.age = age2
        student.bio = bio2
        db.session.commit()

        return redirect(url_for("students"))
    student = Student.query.get(student_id)
    return render_template("studentedit2.html",student=student)

@app.route("/teacheredit/<int:teacher_id>", methods=('GET', 'POST', 'PUT'))
@login_required
def teacheredit(teacher_id):
    if request.method == 'POST':
        teacher = Teacher.query.get(teacher_id)
        
        name2 = request.form['name']
        email2 = request.form['email']
        age2 = int(request.form['age'])
        bio2 = request.form['bio']

        teacher.name = name2
        teacher.email = email2
        teacher.age = age2
        teacher.bio = bio2
        db.session.commit()

        return redirect(url_for("teachers"))
    teacher = Teacher.query.get(teacher_id)
    return render_template("teacheredit.html",teacher=teacher)

@app.route("/teacherdelete/<int:teacher_id>", methods=('GET', 'POST', 'DELETE'))
@login_required
def teacherdelete(teacher_id):
    # if request.method == 'POST':
    #     student = Student.query.get(student_id)
        
    #     db.session.delete(student)
    #     db.session.commit()

    #     return redirect(url_for("students"))
    # student = Student.query.get(student_id)
    # return render_template("studentdelete.html",student=student)
    teacher = Teacher.query.get(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for("teachers"))

@app.route("/studentdelete/<int:student_id>", methods=('GET', 'POST', 'DELETE'))
@login_required
def studentdelete(student_id):
    # if request.method == 'POST':
    #     student = Student.query.get(student_id)
        
    #     db.session.delete(student)
    #     db.session.commit()

    #     return redirect(url_for("students"))
    # student = Student.query.get(student_id)
    # return render_template("studentdelete.html",student=student)
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("students"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods = ['POST'])
def signup_post():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
  
    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name, 
    password=generate_password_hash(password,method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()
    flash("User registered successfully. Please log in.")
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods = ['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    remember = request.form.get('remember')
    user = User.query.filter_by(email=email).first()
  
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for("profile"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/students")
def students():
    student = Student.query.all()
    return render_template("students.html", student = student)

@app.route("/teachers")
def teachers():
    teachers = Teacher.query.all()
    return render_template("teachers.html", teacher = teachers)


# """<h1>Introduction to Shapes </h1>
#     <p>There are many different types of shapes. <span style="color:blue;">2D</span>, <span style="color:red;">3D</span>, and <span style="color:purple;">4D</span> shapes.</p>
#     <div style='background-color:#c0c0c0;padding:10px;border:2px solid red;display:inline-block;'>
#         <img src='https://cdn1.byjus.com/wp-content/uploads/2022/09/Fourier-series-Graph.png' width = 300 height = 200>
#         <p>This is the fourier series. A representation of a function in terms of sine and cosine waves.</p>
#     </div>"""


app.run(debug=True)