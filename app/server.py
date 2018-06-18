from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from pymongo import MongoClient
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
client = MongoClient(os.environ['MONGODB_URI'])
db = client['flask-blog']

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

@app.route("/")
def feed():
    return render_template('feed.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():

    # Create form instance
    form = RegistrationForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        # Add user to database
        newPost = db.users.insert_one({
            "username": form.username.data,
            "password": form.password.data,
            "email": form.email.data
        })

        # For debugging purposes
        print newPost

        # Alert user that they were successfully registered
        flash('Account created for ' + form.username.data + '!', 'success')

        # Redirect user to the home feed
        return redirect(url_for('feed'))

    # render the register html template and form for GET requests to '/register'
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    # Create form instance
    form = LoginForm()

    # Make sure the user's entries are valid
    if form.validate_on_submit():

        # Check that this user is in the database
        if db.users.find_one({"email": form.email.data, "password": form.password.data}):

            # Alert user that login was succesful
            flash('You have been logged in!', 'success')

            # Redirect user to the home feed
            return redirect(url_for('feed'))
        else:

            # Otherwise alert user that login was unsuccessful
            flash('Login Unsuccessful. Please check username and password', 'danger')

    # render the login html template and form for GET requests to '/login'
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
