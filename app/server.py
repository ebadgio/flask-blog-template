from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
import json

# Utilities
from bson.objectid import ObjectId
import os
from PIL import Image
import random

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
from forms import RegistrationForm, LoginForm, NewPostForm, UpdateProfileForm


@login_manager.user_loader
def load_user(user_id):

    # Find user by id
    u = db.users.find_one({
        "_id": ObjectId(user_id)
    })

    if u:
        # Load user in User object format to satisfy Flask's requirements
        return User(u["username"], u["email"], str(u["_id"]), u["profile_picture"])

    return None

def format_posts(raw_posts):
    send = []
    for post in raw_posts:

        # Get the author's user object
        user = db.users.find_one({"username": post['author']})

        # Obtain the profile picture for this user and add it to the post
        post['author_image'] = user['profile_picture']

        # Convert the ObjectId into a string
        post['_id'] = str(post['_id'])

        # Format date to naturally readable form
        post['createdAt'] = ('/').join([str(post['createdAt'].month), str(post['createdAt'].day), str(post['createdAt'].year)])
        
        # Add formatted posts to the list we'll return
        send.append(post)
    return send

@app.route("/", methods=['GET'])
@app.route("/discover", methods=['GET'])
def discover():

    # Get top 8 most recent posts
    posts = db.posts.find().sort("createdAt", DESCENDING).limit(8)

    # Format the posts
    formatted_posts = format_posts(posts)

    return render_template('feed.html', posts=formatted_posts)



@app.route("/next/posts/<int:page>", methods=['GET'])
def more(page):

    # Determine amount of posts to skip in the fetch, so feed is continuous without gaps or repeats
    skip_by = (page - 1) * 8

    # Get the posts
    posts = db.posts.find().sort("createdAt", DESCENDING).skip(skip_by).limit(8)

    # Format posts and send as json to client
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
            "profile_picture": "assets/default_pro_pic.jpg",
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
                user = User(u["username"], u["email"], str(u["_id"]), u["profile_picture"])

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

    return render_template('create_post.html', form=form, legend="New Post", action="/create/post")

@app.route("/u/<string:username>")
def profile(username):

    # Find user in database by username
    u = db.users.find_one({"username": username})

    if u:

        # If user exists, find top 5 most recent posts by that user
        posts = db.posts.find({"author": username}).sort("createdAt", DESCENDING).limit(5)

        # Format post dates
        formatted = format_posts(posts)

        # Render profile page
        return render_template('profile.html', user=u, posts=formatted)


    return render_template('404.html', reason="That user doesn't exist"), 404

def save_picture(form_picture):

    # Generate random sequence of characters to create unique filename
    random_int = random.randint(0,10000)

    # Create file name
    filename = current_user.username + "." + str(random_int) + "." + form_picture.filename

    print filename

    # Create path to image file
    picture_path = os.path.join(app.root_path, 'static/assets', filename)

    # Resize the image to save space
    output_size = (205, 205)

    # Save image to specified path
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return 'assets/' + filename

@app.route("/u/edit/<string:username>", methods=["GET", "POST"])
@login_required
def edit_profile(username):

    # Create form instance
    form = UpdateProfileForm()

    # For post request, check that form was valid
    if form.validate_on_submit():

        # Need the user in dictionary format for db
        user = current_user.get_user_dictionary();

        # Save image if one is uploaded
        if form.picture.data:
            picture_path = save_picture(form.picture.data)
            user['profile_picture'] = picture_path

        # Update fields
        user['email'] = form.email.data

        # Save changes to the user
        db.users.save(user)

        flash('Your account has been updated!', 'success')

        return redirect(url_for('profile', username=user['username']))

    elif request.method == 'GET':

        # Set the field inputs to already have the current email for this user
        form.email.data = current_user.email

    return render_template('edit_profile.html', form=form)

@app.route("/delete/post/<string:post_id>", methods=['POST'])
@login_required
def delete_post(post_id):

    print post_id

    # Find the post to be deleted using the post id
    post = db.posts.find_one({
        "_id": ObjectId(post_id)
    })

    # If the post doesn't exist return 404
    if not post:
        return render_template('404.html', reason="That post doesn't exist"), 404

    # If this user didn't make the post, abort the action
    if post['author'] != current_user.username:
        print post['author'], current_user.username
        abort(403)

    # Post exits and correct user, so delete the post
    db.posts.delete_one({
        "_id": ObjectId(post_id)
    })

    # Notify that it was succesful
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('discover'))

@app.route("/edit/post/<string:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):

    # Find the post to be edited using the post id
    post = db.posts.find_one({
        "_id": ObjectId(post_id)
    })

    print "post", post

    # If the post doesn't exist return 404
    if not post:
        return render_template('404.html', reason="That post doesn't exist"), 404

    # If this user didn't make the post, abort the action
    if post['author'] != current_user.username:
        abort(403)

    # Create form instance
    form = NewPostForm()

    # Ensure form entries are valid
    if form.validate_on_submit():

        # Update fields
        post['title'] = form.title.data
        post['content'] = form.content.data

        # Save changes
        db.posts.update({"_id": post['_id']}, post)

        # Notify user
        flash('Your post has been updated!', 'success')

        return redirect(url_for('discover'))

    elif request.method == 'GET':

        # Set the fields to be the current post data
        form.title.data = post['title']
        form.content.data = post['content']

    return render_template('create_post.html', form=form, legend='Update Post', action='/edit/post/' + post_id)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('discover'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
