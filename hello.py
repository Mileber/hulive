#!/usr/bin/python
#coding:utf-8

from flask import Flask
from flask import render_template
from flask import jsonify
from model_user import db
from service_user import app

@app.route("/")
def hello_world():
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()