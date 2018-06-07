__author__ = "Roy Telles Jr"

import uuid
from src.models.post import Post
import datetime
from src.common.database import Database

class Blog:
    def __init__(self, author, title, description, author_id, _id = None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    # Ask the user to write the new post
    def new_post(self, title, content, date = datetime.datetime.utcnow()):
        post = Post(blog_id = self._id,
                    title = title,
                    content = content,
                    author = self.author,
                    date = date)

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection="blogs", data=self.json())

    def json(self):
        return {
            "author": self.author,
            "author_id": self.author_id,
            "title": self.title,
            "description": self.description,
            "_id": self._id
        }

    '''
    Note: It is easier in the big picture to return objects so that we can make minute changes to the object
          and save it to our blog, without having to perform multiple queries, or get the data, then call methods
          The point of having objects is to use them!
    '''
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection = "blogs", query = {"_id": id})

        # We want to return an object of type Blog so that we can call its methods
        '''
        return cls(author = blog_data["author"],
                    title = blog_data["title"],
                    description = blog_data["description"],
                    _id = blog_data["_id"])
        '''
        # Like in post.py, we can simplify we can simplify the above:
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection = "blogs", query = {"author_id": author_id})

        return [cls(**blog) for blog in blogs] # returns a list of Blog objects

