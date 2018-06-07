__author__ = "Roy Telles Jr"

from src.common.database import Database
import uuid
import datetime

class Post:
    def __init__(self, blog_id, title, content, author, date = datetime.datetime.utcnow(), _id = None):
    # default parameters only at end
        self.blog_id = blog_id # which blog are we in? (i.e. Johns, Ann's, Mark's, etc)
        self.title = title
        self.content = content
        self.author = author
        self.created_date = date
        self._id = uuid.uuid4().hex if _id is None else _id # used to identify the specific post, always unique
        # the uuid4 is a random uuid generator, .hex gives us a 32 character hexadecimal string

        # post = Post(blog_id = "123", title = "a title", content = "some content", author = "Jose")

    def save_to_mongo(self):
        Database.insert(collection = "posts", data = self.json())

    def json(self):
        return {
            "_id": self._id,
            "blog_id": self.blog_id,
            "author": self.author,
            "content": self.content,
            "title": self.title,
            "date": self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection = "posts", query = {"_id": id})
        # Note: "collection = " is not necessary, but it helps

        '''
        return cls(blog_id = post_data["blog_id"],
                   title = post_data["title"],
                   content = post_data["content"],
                   author = post_data["author"],
                   date = post_data["date"],
                   _id = post_data["_id"])
        '''
        # We can simplify the above repetitiveness by:
        return cls(**post_data)
        # This return says:
            # For each element in post_data get the name of teh element when it comes from the database and say
            # that the object's element is equal to that

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection = "posts", query = {"blog_id": id})]
