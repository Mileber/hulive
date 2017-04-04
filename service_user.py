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
from service_stream import app

# 插入新用户
# TODO:头像
@app.route('/liveUser/userInsert/', methods=['POST'])
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
    usr = user(user_info['phone'],user_info['name'], user_info['password'], user_info['stream_key'], user_info['phone'])

    # TODO: 密码加密

    # 将新增项目插入数据库
    db.session.add(usr)

    # 提交修改
    db.session.commit()

    query_user = user.query.filter_by(name=user_info['name']).first()
    if query_user == None:
        ret = {
            'code' : 501,
            'msg' : 'insert fail'
        }
        return jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'insert success',
            'id' : query_user.id,
            'name' : query_user.name,
            'password' : query_user.password,
            'stream_key' : query_user.stream_key,
            'phone' : query_user.phone,
            #'is_up' : query_user.is_up,
            #'avatar_path' : query_user.avatar_path
        }
        return jsonify({'ret':ret})

# 根据id查询用户
# TODO:根据用户名查询
@app.route('/liveUser/userQueryById/', methods=['POST'])
def get_user():
    if not request.json:
        abort(400)
    get_id = request.json['id']
    get = user.query.filter_by(id = get_id).first()

    if get == None:
        ret = {
            'code' : 501,
            'msg' : 'user not found'
        }
        return jsonify({'ret':ret})
    else:
        # 获取表成员属性
        ret = {
            'code' : 101,
            'msg' : 'query success',
            'id' : get.id,
            'name' : get.name,
            'stream_key' : get.stream_key,
            'phone' : get.phone,
            'is_up' : get.is_up,
            'avatar_path' : get.avatar_path
        }
        return jsonify({'ret':ret})

# 更新用户(只允许更新 name, phone)
@app.route('/liveUser/userUpdate/', methods=['POST'])
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

# 上传头像
@app.route('/liveUser/updateAvatar', methods=['POST'])
def update_avatar():
    f = request.files['avatar']
    f.save(os.path.join('/home/projects/hulive/pic', f.filename))
    # Get str object from field of text
    # s = request.form['name']
    # with open('/home/ping/Documents/test.txt', 'a') as f:
        # f.write(s)
    
    avatar_path = os.path.join('/home/projects/hulive/pic' + f.filename)

    ret = {
        'code' : 101,
        'msg' : 'avatar upload success',
        'avatar_path' : avatar_path
    }
    return jsonify({'ret' : ret})

# 登录
@app.route('/liveUser/login/', methods=['POST'])
def login():
    if not request.json:
        abort(400)
    get_phone = request.json['phone']
    get_password = request.json['password']
    get = user.query.filter_by(phone = get_phone).first()

    if get == None:
        # 未查询到返回错误码 501
        ret = {
            'code' : 501,
            'msg' : "phone not found"
        }
        return jsonify({'ret':ret})
    else:
        if get.password == get_password:
            # 获取表成员属性
            ret = {
                'code' : 101,
                'msg' : 'login success',
                'id' : get.id,
                'name' : get.name,
                'stream_key' : get.stream_key,
                'phone' : get.phone
            }
            return jsonify({'ret':ret})
        else:
            ret = {
                'code' : 502,
                'msg' : 'password error'
            }
            return jsonify({'ret':ret})


