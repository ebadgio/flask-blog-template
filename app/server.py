from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
import json

# useful packages
from bson.objectid import ObjectId
import os

# __init__
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Password hashing
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# MongoDB config
from pymongo import MongoClient, DESCENDING
client = MongoClient(os.environ['MONGODB_URI'])
db = client['flask-blog']

# flask_login config
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User model
from models import User

# loging/register forms
from forms import RegistrationForm, LoginForm, NewPostForm


@login_manager.user_loader
def load_user(user_id):
    u = db.users.find_one({
        "_id": ObjectId(user_id)
    })
    if u:
        return User(u["username"], u["email"], str(u["_id"]))

    return None

def format_posts(raw_posts):
    send = []
    for post in raw_posts:
        post['_id'] = str(post['_id'])
        post['createdAt'] = ('/').join([str(post['createdAt'].month), str(post['createdAt'].day), str(post['createdAt'].year)])
        send.append(post)
    return send

@app.route("/", methods=['GET'])
@app.route("/discover", methods=['GET'])
def discover():

    posts = db.posts.find().sort("createdAt", DESCENDING).limit(8)

    formatted_posts = format_posts(posts)

    return render_template('feed.html', posts=formatted_posts)

@app.route("/next/posts/<int:page>", methods=['GET'])
def more(page):

    skip_by = (page - 1) * 8

    posts = db.posts.find().sort("createdAt", DESCENDING).skip(skip_by).limit(8)

    return json.dumps(format_posts(posts))



@app.route("/register", methods=['GET', 'POST'])
def register():

    # Check if user is already logged in
    if current_user.is_authenticated:

        # If they are then send them back to feed
        return redirect(url_for('discover'))

    # Create form instance
    form = RegistrationForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        # Hash password for security
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Add user to database
        newUser = db.users.insert_one({
            "username": form.username.data,
            "password": hashed_password, # Store hashed password in DB
            "email": form.email.data
        })

        # For debugging purposes
        print newUser

        # Alert user that they were successfully registered
        flash('Account created for ' + form.username.data + '! You can now login.', 'success')

        # Redirect user to the home feed
        return redirect(url_for('discover'))

    # render the register html template and form for GET requests to '/register'
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('discover'))

    # Create form instance
    form = LoginForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        # Search database for user by email
        u = db.users.find_one({"email": form.email.data})

        # Check that this user is in the database
        if u:

            # Check that user entered correct password
            if bcrypt.check_password_hash(u["password"], form.password.data):

                # put mongodb user obj into User class for it to work with flask_login
                user = User(u["username"], u["email"], str(u["_id"]))

                # login user with flask_login
                login_user(user, remember=True)

                # Alert user that login was succesful
                flash('You have been logged in!', 'success')

                # Redirect user to the home feed
                return redirect(url_for('discover'))

            # Incorrect password
            else:

                # Notify user
                flash('Login Unsuccessful. Incorrect password. Please check work and try again.', 'danger')

        # Either user entered incorrect email or user is not actually registered
        else:

            # Notify user
            flash('Login Unsuccessful. Email not found. Please try again or Register.', 'danger')

    # render the login html template and form for GET requests to '/login'
    return render_template('login.html', form=form)


@app.route("/create/post", methods=['GET', 'POST'])
@login_required
def new_post():

    # Create form instance
    form = NewPostForm()

    # Check that fields are valid
    if form.validate_on_submit():

        # Submit post to database
        newUser = db.posts.insert_one({
            "author": current_user.username,
            "content": form.content.data,
            "title": form.title.data,
            "createdAt": datetime.now()
        })

        flash('Your post has been created!', 'success')

        return redirect(url_for('discover'))

    return render_template('create_post.html', form=form, legend="New Post")

@app.route("/u/<string:username>")
@login_required
def account(username):

    u = db.users.find_one({"username": username})

    return render_template('account.html', user=u)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('discover'))



if __name__ == '__main__':
    app.run(debug=True)
