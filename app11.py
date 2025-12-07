# app.py

from flask import Flask
from flask_login import LoginManager,login_required
from models import db, User
import config

#for login and singn up
from flask import render_template,redirect,url_for,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user

#core logics
from flask_login import current_user
from models import Task

app = Flask(__name__,template_folder="templates",static_folder="")

# load config
app.config.from_object(config)

# connect db to app
db.init_app(app)

# setup login manager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# user loader (for sessions)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# create tables
with app.app_context():
    db.create_all()

# test route
@app.route("/")
def index():
    return redirect(url_for("login"))


#registeration
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        
        hashed_password=generate_password_hash(password)
        
        user=User(username=username,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("index"))
    return render_template("register.html")

#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form["password"]
        
        user=User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("dashboard"))
        return "Invalid username or password"
    return render_template("login.html")


#dashoard and inserting an task

@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    if request.method=="POST":
        title=request.form["title"]
        description=request.form["description"]
        
        task=Task(
            title=title,
            description=description,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("dashboard"))
    tasks=Task.query.filter_by(user_id=current_user.id)
    return render_template("dashboard.html",tasks=tasks)

#delete 
@app.route("/task/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task=Task.query.get_or_404(task_id)
    
    if task.user_id!=current_user.id:
        return "Unauthorized",403
    db.session.delete(task)
    db.session.commit()
    
    return redirect(url_for("dashboard"))

#update
@app.route("/task/edit/<int:task_id>",methods=["GET","POST"])
@login_required
def edit_task(task_id):
    task=Task.query.get_or_404(task_id)
    
    if task.user_id!=current_user.id:
        return "Unauthorized",403
    if request.method=="POST":
        task.title=request.form["title"]
        task.description=request.form["description"]
        db.session.commit()
        
        return redirect(url_for("dashboard"))
    return render_template("edit_task.html",task=task)

        

#logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))





if __name__ == "__main__":
    app.run(debug=True)
