# web_blog
A web application that simulates a blog posting/creating site

## Development Environment
Utilizing PyCharm, this application utilizes flask and pymongo libraries to simulate a blog posting site on a local server

### Functionality
This application allows a user to create a new post within a blog (currently added manually via backend (i.e using terminal and pymongo to insert blog information into a database)) and access new and current posts by clicking the post's title.

### Description
This is a simple web-based blog that doesn't do much but introduces Flask, HTML, CSS, Bootstrap, Jinja2, and other concepts such as endpoints and APIs.

The blog requires MongoDB to be running without authentication enabled.

Once this is running, execute the app and navigate to the endpoint (default: `http://127.0.0.1:5005/`).

The available endpoints are:

- `/`
- `/login`
- `/register`
- `/blogs`
- `/blogs/new`
- `/posts/<string:blog_id>`
- `/posts/new/<string:blog_id>`
