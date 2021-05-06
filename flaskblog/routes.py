from flask import Flask,render_template,url_for,flash,redirect
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog import app, db, bcrypt
# this import cannot be placed on the top because db has to initiated
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user
posts=[
    {
        'author': 'Carl',
        'title':'Rejoice',
        'date_posted':'12-03-2021',
        'content':'Use Bootstrap’s custom button styles for actions in forms, dialogs, and more with support for multiple sizes, states, and more'
    },
    {
        
        'author': 'Harry',
        'title':'Markin',
        'date_posted':'30-01-2021',
        'content':'FLaskkkskskskadksskaaskdka'
    }
]

# home route
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts,title='home')
 
# about route
@app.route("/about")
def about():
    return render_template('about.html',title='about')
 
# register route
@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # making instance (form) of RegsitrationForm class made in forms.py
    form = RegistrationForm()
    # if content is validated then flashing message 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Login Please','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)
 
# login route
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # making instance (form) of LoginForm class made in forms.py
    form = LoginForm() 
    # if content is validated then flashing message 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'Login successfull!','success')
            return redirect(url_for('home'))
        else:        
            flash(f'Login Unsuccessfull! Please check your E-mail and password ','danger')
            
    return render_template('login.html',title='Login',form=form)
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))