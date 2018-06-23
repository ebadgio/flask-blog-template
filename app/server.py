from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from pymongo import MongoClient
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
client = MongoClient(os.environ['MONGODB_URI'])
db = client['flask-blog']
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
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
def feed():
    return render_template('feed.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create form instance
    form = RegistrationForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        # Add user to database
        newUser = db.users.insert_one({
            "username": form.username.data,
            "password": form.password.data,
            "email": form.email.data
        })

        # For debugging purposes
        print newUser

        # Alert user that they were successfully registered
        flash('Account created for ' + form.username.data + '! You can now login.', 'success')

        # Redirect user to the home feed
        return redirect(url_for('feed'))

    # render the register html template and form for GET requests to '/register'
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create form instance
    form = LoginForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        u = db.users.find_one({"email": form.email.data, "password": form.password.data})

        # Check that this user is in the database
        if u:

            user = User(u["username"], u["email"], str(u["_id"]))

            login_user(user, remember=True)

            # Alert user that login was succesful
            flash('You have been logged in!', 'success')

            # Redirect user to the home feed
            return redirect(url_for('feed'))
        else:

            # Otherwise alert user that login was unsuccessful
            flash('Login Unsuccessful. Please check username and password', 'danger')

    # render the login html template and form for GET requests to '/login'
    return render_template('login.html', title='Login', form=form)

@app.route("/u/<string:username>")
@login_required
def account(username):
    return "<h1>Account page " + username + "<h1/>"

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
