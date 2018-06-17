from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for' + form.username.data + '!', 'success')
        return redirect(url_for('feed'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'badgio1028@gmail.com' and form.password.data == 'eli123':
            flash('You have been logged in!', 'success')
            return redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
