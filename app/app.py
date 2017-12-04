from flask import Flask, request, render_template, redirect, url_for
from .forms import SignupForm
from .models import db
from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()

app = Flask(__name__)
app.secret_key = 'secretkeyhereplease'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/database.sqlite'

@app.route('/protected')
@login_required
def protected():
    return "protected area"

@app.route('/login', methods=['GET','POST'])
def login():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return "User logged in"                
                else:
                    return "Wrong password"            
            else:
                return "user doesn't exist"        
     else:
            return "form not validated"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists" 
            else:
                newuser = User(form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return "User created!!!"        
         else:
             return "Form didn't validate"

def register():
    return "Signup"
def index():
    return "Welcome to Flask"
def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()
if __name__ == '__main__':
    app.init_db()
    app.run(port=5000, host='localhost', debug=True)