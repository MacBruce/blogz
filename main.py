#the majority of the assignment is near identical to user signup that we did
#the videos were very helpful

from flask import Flask, request, redirect, render_template, flash
from isEmpty import *
from flask_sqlalchemy import SQLAlchemy
import cgi

# create runnable app & connect to db
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:doublerainbow@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# create blog model for db
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User')

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.before_request
def require_login():
    routes = ['login', 'register', 'blogs', 'index', 'logout']
    if request.endpoint not in routes and 'email' not in session:
        return redirect('/login')

# # handle home route by redirecting to home page
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     return redirect('/blog')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            if isEmpty(password):
                blank_error = "Must create a password!"
                return render_template('register.html', blank_error=blank_error)
            elif lessThan(password, 4):
                len_error = "Password must be longer than 3 characters"
                return render_template('register.html', len_error=len_error)
            elif password == verify:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('/newpost')
            elif password != verify:
                password_v_error = 'Your passwords do not match, try again.'
                return render_template('register.html', password_v_error=password_v_error)

        else:
            duplicate_error = "User Exists"
            return render_template('register.html', duplicate_error=duplicate_error)
    else:
        return render_template('register.html')



@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #url building
    if request.args:
        post_id = request.args.get('id')
        blog = Blog.query.get(post_id)
        return render_template('singlepost.html', blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    title_er = 'Your blog needs a title'
    body_er = 'Your blog needs a body'

# didnt want to use flash as it is a bain to my existance
    if request.method == 'POST':
        sessionOwner = User.query.filter_by(email = session['email']).first()
        #grab data from forms
        blog_title = request.form['title']
        blog_body = request.form['body']

        session_list = []
        # holding info to temporarily display
        session_list.append(sessionOwner)

        if isEmpty(blog_title) and isEmpty(blog_body):
            return render_template('newpost.html', title_er=title_er, body_er=body_er)
        elif isEmpty(blog_title) or isEmpty(blog_body):
            if isEmpty(blog_title):
                return render_template('newpost.html', title_er=title_er)
            return render_template('newpost.html', body_er = body_er)
        else:
            new_blog = Blog(blog_title, blog_body, sessionOwner)
            db.session.add(new_blog)
            db.session.commit()
            session_id = Blog.query.order_by('-id').first()
            dynamic_str = "?id=" + str(session_id.id)

            return redirect('/blog' + dynamic_str)

    return render_template('newpost.html')

@app.route('/logout')
def logout():

    if 'email' in session:
        del session['email']
        logout_success = "You have logged out"
    return redirect('/blogs')





if __name__ == '__main__':
    app.run()
