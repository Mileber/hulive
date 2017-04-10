#!/usr/bin/python
#coding:utf-8

import pili
import time
import json
import config
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from info import database_url
from info import accessKey
from info import secretKey
from info import hubName
from sqlalchemy.inspection import inspect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    stream_key = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(15), unique=True)
    #is_up = db.Column(db.Boolean, nullable=False)
    #avatar_path = db.Column(db.String(50))

    # def __init__(self, id, name, password, stream_key, phone):
        # self.id = id
        # self.name = name
        # self.password = password
        # self.stream_key = stream_key
        # self.phone = phone
        #self.is_up = is_up
        #self.avatar_path = avatar_path
    
    def __repr__(self):
        return '{"id":%d, "name":%s}' % (self.id, self.name)

class Stream(db.Model):
    stream_key = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(50))
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, stream_key, title, level):
        self.stream_key = stream_key
        self.title = title
        self.level = level

    def __repr__(self):
        return '{"stream_key":%s, "title":%s, "level":%d}' % (self.stream_key, self.title, self.level)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    from_user_id = db.Column(db.Integer, nullable=False)
    to_user_id = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id, 
            'from_id': self.from_user_id,
            'to_id': self.to_user_id,
        }

class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '%s, %s' % (self.name, self.value)

db.create_all()

@app.route("/")
def hello_world():
    return 'Hello World'

# 插入新用户
# TODO:头像
@app.route('/liveUser/userInsert/', methods=['POST'])
def insert_user():
    if not request.json:
        return "failed!", 400
    user_info = {
        'name' : request.json['name'],
        'password' : request.json['password'],
        'stream_key' : request.json['stream_key'],
        'phone' : request.json['phone']
    }

    # 初始化user对象
    #usr = User(int(user_info['id']),user_info['name'], user_info['password'], user_info['stream_key'], user_info['phone'])
    usr = User()
    usr.name = user_info['name']
    usr.password = user_info['password']
    usr.stream_key = user_info['stream_key']
    usr.phone = user_info['phone']

    # TODO: 密码加密

    # 将新增项目插入数据库
    db.session.add(usr)

    # 提交修改
    db.session.commit()

    query_user = User.query.filter_by(name=user_info['name']).first()
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
@app.route('/liveUser/userQueryById/', methods=['POST'])
def get_user():
    if not request.json:
        abort(400)
    get_id = request.json['id']
    get = User.query.filter_by(id = get_id).first()

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
            #'is_up' : get.is_up,
            #'avatar_path' : get.avatar_path
        }
        return jsonify({'ret':ret})

# 根据stream_key查询用户
@app.route('/liveUser/userQueryByKey', methods=['POST'])
def get_user_by_key():
    if not request.json:
        abort(400)
    get_key = request.json['stream_key']
    result = User.query.filter_by(stream_key = get_key).first()

    if result == None:
        ret = {
            'code' : 501,
            'msg' : 'user not found'
        }
        return jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'query success',
            'id' : result.id,
            'name' : result.name,
            'stream_key' : result.stream_key,
            'phone' : result.phone
        }
        return jsonify({'ret':ret})

# 根据name查询用户
@app.route('/liveUser/userQueryByName', methods=['POST'])
def get_user_by_name():
    if not request.json:
        abort(400)
    get_name = request.json['name']
    result = User.query.filter_by(name = get_name).first()

    if result == None:
        ret = {
            'code' : 501,
            'msg' : 'user not found'
        }
        return jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'query success',
            'id' : result.id,
            'name' : result.name,
            'stream_key' : result.stream_key,
            'phone' : result.phone
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

    user_query = User.query.filter_by(id=user_info['id']).first()
    if user_query == None:
        return "user id error"
    else:
        name_query = User.query.filter_by(name=user_info['name']).first()
        phone_query = User.query.filter_by(phone=user_info['phone']).first()

        if user_info['name'] == user_query.name:
            if user_info['phone'] == user_query.phone:
                return "name or phone has been used"
            else:
                user_query.phone = user_info['phone']
                db.session.commit()
                ret = {
                    'code' : 101,
                    'msg' : 'update success',
                    'id' : user_query.id,
                    'name' : user_query.name,
                    'stream_key' : user_query.stream_key,
                    'phone' : user_query.phone
                }
                return jsonify({'ret':ret})
        else:
            user_query.name = user_info['name']
            db.session.commit()
            ret = {
                'code' : 101,
                'msg' : 'update success',
                'id' : user_query.id,
                'name' : user_query.name,
                'stream_key' : user_query.stream_key,
                'phone' : user_query.phone
            }
            return jsonify({'ret':ret})

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
    get = User.query.filter_by(phone = get_phone).first()

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

    live = Stream(live_info['stream_key'], live_info['title'], live_info['level'])

    db.session.add(live)
    db.session.commit()

    query_stream = Stream.query.filter_by(stream_key=live_info['stream_key']).first()
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

    stream_query = Stream.query.filter_by(stream_key=get_live['stream_key']).first()
    if stream_query == None:
        ret = {
            'code' : 501,
            'msg' : 'stream key error'
        }
        return jsonify({'ret':ret})
    else:
        live = Stream(get_live['stream_key'], get_live['title'], get_live['level'])
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
    get = Stream.query.filter_by(stream_key = stream_query).first()

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

# 查询关注列表及人数
# 参数：user_id
@app.route('/huli/getFollowList/', methods=['POST'])
def get_follow_list():
    if not request.json:
        abort(400)
    
    user_id = request.json['user_id']
    follow_list = Follow.query.filter_by(from_user_id = user_id).all()
    print follow_list
    follow_num = Follow.query.filter_by(from_user_id = user_id).count()

    if follow_list == None:
        ret = {
            'code' : 501,
            'msg' : 'follow list not found'
        }
        return jsonify({'ret':ret})
    else:
        '''
        ret = {
            'code' : 101,
            'msg' : 'query follow list success',
            'num' : follow_num,
            'list' : follow_list
        }
        '''
        
        return jsonify(follows=[e.serialize() for e in follow_list])

# 查询粉丝列表
# 参数：user_id
@app.route('/huli/getFansList/', methods=['POST'])
def get_fans_list():
    if not request.json:
        abort(400)

    user_id = request.json['user_id']
    fans_list = Follow.query.filter_by(to_user_id = user_id).all()
    fans_num = Follow.query.filter_by(to_user_id = user_id).count()

    if fans_list == None:
        ret = {
            'code' : 501,
            'msg' : 'fans list not found'
        }
        return jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'query fans list success',
            'num' : fans_num,
            'list' : fans_list
        }
        return jsonify({'ret':ret})

# 查询from_id是否关注to_id
# 参数：from_id, to_id
@app.route('/huli/isFollow/', methods=['POST'])
def is_follow():
    if not request.json:
        abort(400)
    
    from_id = request.json['from_id']
    to_id = request.json['to_id']
    result = Follow.query.filter_by(from_user_id=from_id, to_user_id=to_id).first()

    if result == None:
        ret = {
            'code' : 501,
            'msg' : 'not followed'
        }
        return jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'following',
            'from_id' : result.from_user_id,
            'to_id' : result.to_user_id
        }
        return jsonify({'ret':ret})

# 新增关注
# 参数：from_id, to_id
@app.route('/huli/insertFollow/', methods=['POST'])
def insert_follow():
    if not request.json:
        abort(400)
    follow = {
        'from_id' : request.json['from_id'],
        'to_id' : request.json['to_id']
    }

    follow_item = Follow()
    follow_item.from_user_id = follow["from_id"]
    follow_item.to_user_id = follow["to_id"]

    db.session.add(follow_item)

    db.session.commit()

    query_follow = Follow.query.filter_by(from_user_id=follow['from_id'], to_user_id=follow['to_id']).first()
    if query_follow == None:
        ret = {
            'code' : 501,
            'msg' : 'insert fail'
        }
        return jsonify({'ret':ret})
    else:
        ret = {
            'code' : 101,
            'msg' : 'insert success',
            'id' : query_follow.id,
            'from_user_id' : query_follow.from_user_id,
            'to_user_id' : query_follow.to_user_id
        }
        return jsonify({'ret':ret})

# 取消关注
# 参数：from_id, to_id
@app.route('/huli/deleteFollow/', methods=['POST'])
def delete_follow():
    if not request.json:
        abort(400)
    get = {
        'from_id' : request.json['from_id'],
        'to_id' : request.json['to_id']
    }

    query_follow = Follow.query.filter_by(from_user_id=get['from_id'], to_user_id=get['to_id']).first()

    if query_follow == None:
        ret = {
            'code' : 501,
            'msg' : 'follow not found'
        }
        return jsonify({'ret':ret})
    else:
        follow_item = Follow()
        follow_item.from_user_id = get["from_id"]
        follow_item.to_user_id = get["to_id"]
        db.session.delete(follow_item)
        db.session.commit()
        query_follow_new = Follow.query.filter_by(from_user_id=get['from_id'], to_user_id=get['to_id']).first()
        if query_follow_new == None:
            ret = {
                'code' : 101,
                'msg' : 'delete follow success'
            }
            return jsonify({'ret':ret})
        else:
            ret = {
                'code' : 501,
                'msg' : 'delete follow failed'
            }
            return jsonify({'ret':ret})




mac = pili.Mac(accessKey, secretKey)
client = pili.Client(mac)
hub = client.hub("derya")
# key = "streamKey2"
# key由uid生成
      
# 1.生成带授权凭证的 RTMP 推流地址
# 参数：key
@app.route('/huli/getRTMPPublishURL/', methods=['POST'])
def get_rtmp_publish():
    if not request.json:
        abort(400)
    key = request.json['key']
    rtmp_publish = pili.rtmp_publish_url("pili-publish.pearapple.net", hubName, key, mac, 60) 
    up = {
        'user_key' : key,
        'rtmp_publish' : rtmp_publish
    }
    return jsonify(up)

# 2.生成 RTMP 播放地址
# 参数：key
@app.route('/huli/getRTMPPlayURL/', methods=['POST'])
def get_rtmp_play():
    if not request.json or not 'key' in request.json:
    	abort(400)
    key = request.json['key']
    rtmp_play = pili.rtmp_play_url("pili-live-rtmp.pearapple.net", hubName, key)
    up = {
        'user_key' : key,
        'rtmp_play' : rtmp_play
    }
    return jsonify(up)

# 3.生成 HLS 播放地址
# 参数：key
@app.route('/huli/getHLSPlayURL/', methods=['POST'])
def get_hls_play():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    hls_play = pili.hls_play_url("pili-live-hls.pearapple.net", hubName, key)
    up = {
        'user_key' : key,
        'hls_play' : hls_play
    }
    return jsonify(up)

# 4.生成 HDL(HTTP-FLV) 播放地址
# 参数：key
@app.route('/huli/getHDLPlayURL/', methods=['POST'])
def get_hdl_play():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    hdl_play = pili.hdl_play_url("pili-live-hdl.pearapple.net", hubName, key)
    up = {
        'user_key' : key,
        'hdl_play' : hdl_play
    }
    return jsonify(up)

# 5.生成直播封面地址
# 参数：key
@app.route('/huli/getSnapshotPlayURL/', methods=['POST'])
def get_snapshot_play():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    snapshot_play = pili.snapshot_play_url("pili-live-snapshot.pearapple.net", hubName, key)
    up = {
        'user_key' : key,
        'snapshot_play' : snapshot_play
    }
    return jsonify(up)

# 6.创建流
# 参数：key
@app.route('/huli/createStream/', methods=['POST'])
def create_stream():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.create(key)
    return stream.to_json()

# 7.获得流
# 参数：key
@app.route('/huli/getStream/', methods=['POST'])
def get_stream():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    return stream.to_json()

# 8.查询流列表
@app.route('/huli/getStreamList/', methods=['GET'])
def get_stream_list():
    # TODO:prefix 不知道是啥
    #stream_pre = ""
    stream_list = hub.list(limit=2)
    stream_list_json = json.dumps(stream_list)
    return stream_list_json

# 9.查询直播列表
@app.route('/huli/getStreamListLive/', methods=['GET'])
def get_stream_list_live():
    stream_list_live = hub.list(liveonly=True)
    stream_list_live_json = json.dumps(stream_list_live)
    return stream_list_live_json
    
# 10.查询流信息
# 参数：key
@app.route('/huli/getStreamInfo/', methods=['POST'])
def get_stream_info():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    return stream.to_json()

# 11.禁播流
# 参数：key，time
@app.route('/huli/disableStream/', methods=['POST'])
def disable_stream():
    if not request.json or not 'key' in request.json or not 'time' in request.json: 
        abort(400)
    key = request.json['key']
    time = request.json['time']
    stream = hub.get(key)
    if(stream.disabled()):
        return jsonify({
            'msg' : "stream is alreadly disabled"
        })
    else:
        stream.disable(int(time.time()) + time)
        #print "after call disable:", stream.refresh(), stream.disabled()
        return jsonify({
            'msg' : "stream disable success"
        })

# 12.启用流
# 参数：key
@app.route('/huli/enableStream/', methods=['POST'])
def enable_stream():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    stream.enable()
    return jsonify({
            'msg' : "stream enable success"
        })

# 13.查询直播实时信息
# 参数：key
@app.route('/huli/getLiveStatus/', methods=['POST'])
def get_live_status():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    live_status = stream.status()
    return live_status.to_json()

# 14.保存直播回放
# 参数：key
@app.route('/huli/Save/', methods=['POST'])
def save_playback():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    now = int(time.time())
    playback = stream.saveas(start_second=now-300, fname=key+now+"_save.m3u8")
    return playback.to_json()

# 15.查询直播历史记录
# 参数：key
@app.route('/huli/getHistoryActivity/', methods=['POST'])
def get_history_activity():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    now = int(time.time())
    history_activity = stream.history(start_second=now-86400)
    return history_activity.to_json()


# 16.开始
@app.route('/huli/start/', methods=['POST'])
def start():
    if not request.json:
        abort(400)
    key = request.json['key']
    stream = hub.get(key)
    stream.start()
    return "stream started"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)