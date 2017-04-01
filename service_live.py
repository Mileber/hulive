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
from service_user import app

# 插入stream相关
@app.route('/liveInfo/streamInsert/', methods=['POST'])
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
        ret = {
            'code' : 501,
            'msg' : 'insert fail'
        }
        return  jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'insert success',
            'stream_key' : query_stream.stream_key,
            'title' : query_stream.title,
            'level' : query_stream.level
        }
        return jsonify({'ret':ret})

# 更新
@app.route('/liveInfo/streamUpdate/', methods=['POST'])
def update_stream():
    if not request.json:
        return "failed", 400
    
    get_live = {
        'stream_key' : request.json['stream_key'],
        'title' : request.json['title'],
        'level' : request.json['level']
    }

    stream_query = stream.query.filter_by(stream_key=get_live['stream_key']).first()
    if stream_query == None:
        ret = {
            'code' : 501,
            'msg' : 'stream key error'
        }
        return jsonify({'ret':ret})
    else:
        live = stream(get_live['stream_key'], get_live['title'], get_live['level'])
        db.session.commit()
        ret = {
            'code' : 101,
            'msg' : 'change stream info success',
            'stream_key' : get_live['stream_key'],
            'title' : get_live['title'],
            'level' : get_live['level']
        }
        return jsonify({'ret':ret})

# 根据stream_key查询
@app.route('/liveInfo/streamQuery/', methods=['POST'])
def get_live_info():
    if not request.json:
        return "failed", 400
    
    stream_query = request.json['stream_key']
    get = stream.query.filter_by(stream_key = stream_query).first()

    if get == None:
        ret = {
            'code' : 501,
            'msg' : 'stream info not found'
        }
    else:
        ret = {
            'code' : 101,
            'msg' : 'query stream info success',
            'stream_key' : get.stream_key,
            'title' : get.title,
            'level' : get.level
        }
    return jsonify({
        'ret' : ret
    })


