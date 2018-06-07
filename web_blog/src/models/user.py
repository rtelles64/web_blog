__author__ = "Roy Telles Jr"

from src.common.database import Database
import uuid
from flask import session
from src.models.blog import Blog
import datetime

class User:
    def __init__(self, email, password, _id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email}) # will return None if we can't find a matching email

        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})  # will return None if we can't find a matching email

        if data is not None:
            return cls(**data)

    @staticmethod # we use static when the method doesn't need "self" for anything
    def login_valid(email, password):
        # Check whether user's email matches password
        user = User.get_by_email(email)

        if user is not None:
            # Check the password
            return user.password == password

        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)

        if user is None:
            # User doesn't exist, so create it
            #new_user = User(email, password) # Since we're using a User (this class) object, we can make this a
                                              # class method!
            new_user = cls(email, password)
            new_user.save_to_mongo() # Will return None
            session["email"] = email # session utilizes cookies, thus Flask handles cookies for us

            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session["email"] = user_email

    @staticmethod
    def logout():
        session["email"] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id) # Now we find by author id

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author = self.email, title = title, description = description, author_id = self._id)

        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date = datetime.datetime.utcnow()):
        # title, content, date = datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id) # We need to consider the blog the user is writing to, blog_id sent
                                        # by website
        blog.new_post(title = title, content = content, date = date)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password # we can only send passwords if the application communicates with itself
            # Note: SENDING PASSWORDS OVER NETWORK IS NEVER SAFE
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())