from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
