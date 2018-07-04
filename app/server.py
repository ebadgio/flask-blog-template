from flask import Flask, render_template, url_for, flash, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

# loging/register forms
from forms import RegistrationForm, LoginForm

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
from pymongo import MongoClient
client = MongoClient(os.environ['MONGODB_URI'])
db = client['flask-blog']

# flask_login config
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User model
from models import User

# Dummy data posts
posts = [
    {
        'author': 'Eli Badgio',
        'title': 'First Blog Post',
        'content': 'Some simple content.',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Simon Sheintoch',
        'title': 'Second Blog Post',
        'content': 'Some other content!',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Eli Badgio',
        'title': 'First Blog Post',
        'content': 'Some simple content.',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Simon Sheintoch',
        'title': 'Second Blog Post',
        'content': 'Some other content!',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Eli Badgio',
        'title': 'First Blog Post',
        'content': 'Some simple content.',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Simon Sheintoch',
        'title': 'Second Blog Post',
        'content': 'Some other content!',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Eli Badgio',
        'title': 'First Blog Post',
        'content': 'Some simple content.',
        'date_posted': 'June 16, 2018'
    },
    {
        'author': 'Simon Sheintoch',
        'title': 'Second Blog Post',
        'content': 'Some other content!',
        'date_posted': 'June 16, 2018'
    }
]

@login_manager.user_loader
def load_user(user_id):
    u = db.users.find_one({
        "_id": ObjectId(user_id)
    })
    if u:
        return User(u["username"], u["email"], str(u["_id"]))

    return None

@app.route("/")
@app.route("/home")
def feed():
    return render_template('feed.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():

    # Check if user is already logged in
    if current_user.is_authenticated:

        # If they are then send them back to feed
        return redirect(url_for('home'))

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
        return redirect(url_for('feed'))

    # render the register html template and form for GET requests to '/register'
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create form instance
    form = LoginForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        # Search database for user by email
        u = db.users.find_one({"email": form.email.data})

        # Check that this user is in the database
        if u:

            # Check that user entered correct password
            if bcrypt.check_password_hash(u.password, form.password.data):

                # put mongodb user obj into User class for it to work with flask_login
                user = User(u["username"], u["email"], str(u["_id"]))

                # login user with flask_login
                login_user(user, remember=True)

                # Alert user that login was succesful
                flash('You have been logged in!', 'success')

                # Redirect user to the home feed
                return redirect(url_for('feed'))

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



@app.route("/u/<string:username>")
@login_required
def account(username):

    u = db.users.find_one({"username": username})

    return render_template('account.html', user=u)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
