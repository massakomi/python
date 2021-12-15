from flask import Flask, request, make_response, render_template, jsonify, session, redirect, url_for, flash

import pymysql
import re

#from functions import getData
from forms import ContactForm, LoginForm

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,  check_password_hash # хеширования пароля при регистрации
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

#from werkzeug.datastructures import MultiDict  для ContactForm

connection = pymysql.connect(host='localhost',
        user='root',
        password='root',
        db='blog',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key' # нужно для сессии
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db нужен чтобы первоначально создать юзера, для регистрации
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
	    self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password_hash, password)


"""
#db.create_all()

u1 = User(username='spike', email='spike@example.com')
u1.set_password("spike")

u2 = User(username='tyke', email='tyke@example.com')
u2.set_password("tyke")

db.session.add_all([u1, u2])
db.session.commit()

res = u1.check_password("spike")
print(res)

"""


login_manager = LoginManager(app)
login_manager.login_view = 'login' # куда перебрасывать в случае login_required
login_manager.login_message = 'Пожалуйста, авторизуйтесь' # сообщение в get_flashed_messages twig

# загружает пользователя в куки сессии, пользователь доступен в current_user
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

# декоратор login_required служит для защиты страниц с помощью Flask-login
@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        # делается запрос в БД через класс User, по имени фильтруем первый элемент
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


"""
@app.route('/login/')
def login():
    return render_template('login.html')
"""

@app.route('/registration/', methods=['post', 'get'])
def registration():

    title = 'Регистрация'
    message = ''
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        message = 'ok'
        if len(username) == 0 or len(password) == 0:
            message = "Empty username or password"
        elif re.search('[^a-z\d]', username):
            message = "Wrong username"
        else:
            user = db.session.query(User).filter(User.email == email).first()
            if user:
                message = "Already exists email"
            else:
                u = User(username=username, email=email)
                u.set_password(password)
                db.session.add(u)
                db.session.commit()

    return render_template('registration.html', **locals())

#index
@app.route('/')
def indexpage():
    content = 1
    #content = printTable('SELECT * FROM blog')
    return render_template('index.html', output=content)

@app.route('/contact/')
def index():
    form1 = ContactForm(MultiDict([('name', 'jerry'),('email', 'jerry@mail.com'),('message', 'xxx')]), meta={'csrf': False})
    res = form1.validate()
    #return jsonify(message="user saved!"), 200
    return render_template('index.html', output=form1.errors)

@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id)


#print(app.url_map)
#print(request.method)





if __name__ == "__main__":
    app.run(debug=True)