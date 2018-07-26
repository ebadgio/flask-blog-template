from server import db
from bson.objectid import ObjectId

"""
User class instance. Necessary for providing flask_login a user with
the required attributes
"""
class User():

    def __init__(self, username, email, id, profile_picture):
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self._id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self._id

    def get_user_dictionary(self):
        return {
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "_id": ObjectId(self._id)
        }

