from flask import Flask, request, make_response, render_template

import pymysql
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

"""
connection = pymysql.connect(host='localhost',
        user='root',
        password='root',
        db='blog',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
"""

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    def __repr__(self):
	    return "<{}:{}>".format(self.id,  self.title[:10])

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='category')
    def __repr__(self):
	    return "<{}:{}>".format(id, self.name)

class  Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on  =  db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
	    return "<{}:{}>".format(id, self.name)

class  Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on  =  db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
	    return "<{}:{}>".format(id, self.name)

# db.create_all()
# c1 = Category(name='Python',  slug='python')
# db.session.add(c1)
# db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)