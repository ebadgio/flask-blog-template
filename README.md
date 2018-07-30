# flask-blog-template
This is a basic blogging app template developed with Python Flask on the backend. I made it simply to learn how to use the Python Flask framework, but after finishing, I figured someone might find it useful as a starting point/template for their app. Primary features of the template: user authentication, basic user profile including profile picture uploads, creating/editing/deleting posts, and loading posts to a central newsfeed.

**Technologies used:** 
   * Python Flask
   * HTML templating with Jinja2
   * CSS3 styling
   * Minimal javascript used for post feed loading
   * MongoDB database


## Usage
1. Fork the repository, clone it, and cd into the directory

1. Resolve the dependencies:
   * `pip install flask flask_login bson flask_bcrypt pymongo flask_wtf wtforms pillow`

1. Set up a mongo database instance. My provider of choice is [mLab](https://www.mlab.com)

1. Set expected environmental variables:
   * SECRET_KEY: some random text will suffice
   * FLASK_ENV: "development"
   * FLASK_APP: the name of the file which initializes the flask app (in this case it is server.py but you can change that)
   * MONGODB_URI: the database uri for the mongo instance
   * *Note: for your convenience, you should consider creating a bash script file (such as env.sh) and set all of the  environmental variables there. Then each time to start development. You simply need to source the file with the command `source env.sh` and the enviormental variables will be set for you.*

1. Start up the server: `flask run`

1. Navigate to localhost:5000

