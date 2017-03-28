#!/usr/bin/python
#coding:utf-8

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import make_response
from model_user import db
from model_user import User as user
from model_user import Stream as stream
from serverApi import app

# 插入新用户
@app.route('/userInsert/', methods=['POST'])
def insert_user():
    if not request.json:
        return "failed!", 400
    user_info = {
        'id' : request.json['id'],
        'name' : request.json['name'],
        'password' : request.json['password'],
        'stream_key' : request.json['stream_key'],
        'phone' : request.json['phone']
    }

    # 初始化user对象
    usr = user(int(user_info['id']), user_info['name'], user_info['password'], user_info['stream_key'], user_info['phone'])

    # TODO: 密码加密

    # 将新增项目插入数据库
    db.session.add(usr)

    # 提交修改
    db.session.commit()

    query_user = user.query.filter_by(name=user_info['name']).first()
    if query_user == None:
        return "insert fail" 
    else:
        return "insert success"

# 根据id查询用户
@app.route('/userQuery/', methods=['POST'])
def get_user():
    if not request.json:
        abort(400)
    get_id = request.json['id']
    get = user.query.filter_by(id = get_id).first()

    # 获取表成员属性
    ret = 'id=%d,name=%s,stream_key=%s,phone=%s' % (get.id, get.name, get.stream_key, get.phone)
    return ret

# 更新用户(只允许更新 name, phone)
@app.route('/userUpdate/', methods=['POST'])
def update_user():
    if not request.json:
        abort(400)
    
    user_info = {
        'id' : request.json['id'],
        'name' : request.json['name'],
        'password' : request.json['password'],
        'stream_key' : request.json['stream_key'],
        'phone' : request.json['phone']
    }

    user_query = user.query.filter_by(id=user_info['id']).first()
    if user_query == None:
        return "user id error"
    else:
        name_query = user.query.filter_by(name=user_info['name']).first()
        phone_query = user.query.filter_by(phone=user_info['phone']).first()

        if user_info['name'] == user_query.name:
            if user_info['phone'] == user_query.phone:
                return "name or phone has been used"
            else:
                user_query.phone = user_info['phone']
                db.session.commit()
                return "phone changed"
        else:
            user_query.name = user_info['name']
            db.session.commit()
            return "name changed"
    
    
    
    
# 插入stream相关
@app.route('/streamInsert/', methods=['POST'])
def insert_stream():
    if not request.json:
        return "failed", 400

    live_info = {
        'stream_key' : request.json['stream_key'],
        'title' : request.json['title'],
        'level' : request.json['level']
    }

    live = stream(live_info['stream_key'], live_info['title'], live_info['level'])

    db.session.add(live)
    db.session.commit()

    query_stream = stream.query.filter_by(stream_key=live_info['stream_key']).first()
    if query_stream == None:
        return "insert fail" 
    else:
        return "insert success"

# 更新
@app.route('/streamUpdate/', methods=['POST'])
def update_stream():
    if not request.json:
        return "failed", 400
    
    get_live = {
        'stream_key' : request.json['stream_key'],
        'title' : request.json['title'],
        'level' : request.json['level']
    }

    stream_query = stream.query.filter_by(stream_key=user_info['stream_key']).first()
    if stream_query == None:
        return "stream key error"
    else:
        live = stream(live_info['stream_key'], live_info['title'], live_info['level'])
        db.session.commit()
        return "change stream info success"

# 根据stream_key查询
@app.route('/streamQuery/', methods=['POST'])
def get_live_info():
    if not request.json:
        return "failed", 400
    
    stream_query = request.json['stream_key']
    get = stream.query.filter_by(stream_key = stream_query).first()

    # 获取表成员属性
    ret = 'stream_key=%s, title=%s, level=%d' % (get.stream_key, get.title, get.level)
    return ret


