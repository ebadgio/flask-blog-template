from server import db

"""
User class instance. Necessary for providing flask_login a user with
the required attributes
"""
class User():

    def __init__(self, username, email, id):
        self.username = username
        self.email = email
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
