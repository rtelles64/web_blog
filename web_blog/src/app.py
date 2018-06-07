__author__ = "Roy Telles Jr"

'''
Here we develop our own API
'''

from flask import Flask, render_template, request, session, make_response
from src.models.user import User
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post

app = Flask(__name__) # "__main__"

''' When we get a "secret key needs to be set error" '''
app.secret_key = "roy" ''' Current not secure!!! Need to change when deploying to internet '''

'''
@app.route('/') # 127.0.0.1:5005/ <- this is the endpoint
def hello_method():
    return render_template("login.html") # Flask knows our login.html file lives
                                         # in a template folder
'''
@app.route('/')
def home_template():
    return render_template("home.html")

@app.route('/login') # 127.0.0.1:5005/login <- this is the endpoint
def login_template():
    return render_template("login.html")

@app.route('/register') # 127.0.0.1:5005/register <- this is the endpoint
def register_template():
    return render_template("register.html")

# Need to initialize database!
@app.before_first_request # offered by Flask, will run initialize_database before
                          # first request
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods = ["POST"]) # We only accept Post requests
# Get user's info (email, password) and log the user in if that info is valid
def login_user():
    email = request.form["email"]
    password = request.form["password"]

    if User.login_valid(email, password):
        User.login(email)
    else: # Need to handle case where user info not valid
        session["email"] = None

    return render_template("profile.html", email = session["email"])

@app.route('/auth/register', methods = ["POST"]) # Allow the users to register
def register_user():
    email = request.form["email"]
    password = request.form["password"]

    User.register(email, password)

    return render_template("profile.html", email = session["email"])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id = None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session["email"])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs = blogs, email = user.email)

@app.route('/blogs/new', methods = ['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template("new_blog.html")
    else:
        title = request.form["title"]
        description = request.form["description"]
        user = User.get_by_email(session["email"])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template("posts.html", posts = posts, blog_title = blog.title, blog_id = blog._id)

@app.route('/posts/new/<string:blog_id>', methods = ['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template("new_post.html", blog_id = blog_id)
    else:
        title = request.form["title"]
        content = request.form["content"]
        user = User.get_by_email(session["email"])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

if __name__ == "__main__":
    app.run(port = 5005) # output: Running on "http://127.0.0.1:5000/" This can be customized by using app.run(port = 4995
              #  or something else)
    '''
    After accessing this through a webpage, we get this output:
    
    127.0.0.1 - - [05/Jun/2018 23:46:06] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [05/Jun/2018 23:46:06] "GET /favicon.ico HTTP/1.1" 404 -
    
    And our webpage displays "Hello, world!"
    '''
