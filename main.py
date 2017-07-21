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

@app.route('/signup', methods = ['POST', 'Get'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if isEmpty(username) or isEmpty(password) or isEmpty(verify):
            flash('Invalid credentials, please try again')
            return redirect('/signup')

        if lessThan(username, 3) or greaterThan(username, 20) or isSpace(username):
            flash('Invalid username, must be 3-20 charecters long without spaces')
            return redirect('/signup')

        if lessThan(password, 3) or greaterThan(password, 20) or isSpace(password):
            flash('Invalid password, must be 3-20 charecters without spaces. ')
            return redirect('/signup')

        if password != verify:
            flash('Your passwords do not match, try again')
            return redirect('/signup')

        else:
            users = User.query.filter_by(username=username).first()

            if users:
                flash('Your username has been taken, please sign in or create an account')
                return redirect('/sigup')

            else:
                nUser = User(email = email, password = password)
                db.session.add(nUser)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')

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


    if request.method == 'POST':
        sessionOwner = User.query.filter_by(email = session['email']).first()
        #grab data from forms
        blog_title = request.form['title']
        blog_body = request.form['body']

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

      




if __name__ == '__main__':
    app.run()

