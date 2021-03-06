
import secrets
# library to set directory while storing files
import os
# library to resize image
from PIL import Image
from flask import Flask,render_template,url_for,flash,redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required

# home route
@app.route("/")
@app.route("/home")
def home():
    # next two lines refer pagination process
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5,)
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
    # checking user already logged in then he will be redirected to home route 
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # making instance (form) of LoginForm class made in forms.py
    form = LoginForm()

    # checking if form is valid or not
    if form.validate_on_submit():
        # creating user variable
        user = User.query.filter_by(email=form.email.data).first()
        # upon log in if such user exists AND the password matches then login granted
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'Login successfull!','success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:        
            flash(f'Login Unsuccessfull! Please check your E-mail and password ','danger')
            
    return render_template('login.html',title='Login',form=form)
 
# logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# func for saving a picture in local
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    i= Image.open(form_picture)
    i.thumbnail([125,125],Image.ANTIALIAS)
    i.save(picture_path)
    return picture_fn

# account route
@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    # validating and then updating the databse with new form data
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    
    # if the page is normaly accessed then existing user data is shown
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file, form=form)

# route to create new post
@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Posted!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form = form,legend='Update Post')

# route to open particular post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# route to update existing post
@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # checking if its the same author or not
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',form = form,legend='Update Post')

# route to delete existing post
@app.route("/post/<int:post_id>/delete",methods=['GET','POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # checking if its the same author or not
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).\
            order_by(Post.date_posted.desc()).\
            paginate(page=page,per_page=5,)
    return render_template('user_posts.html',posts=posts,title='User Posts',user=user)