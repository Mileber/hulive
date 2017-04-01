#!/usr/bin/python
#coding:utf-8
## HuliLive服务端

import pili
import time
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
import json

app = Flask(__name__)

# 密钥使用七牛账号登录 https://portal.qiniu.com/user/key 获取
accessKey = "wFF33ksNJZ3gQCQEEQDPdIKLBwjL-oRaiD-G6Ifv"
secretKey = "PbvgSGmRshsExi6fiEGavPaWVCvFgvxJKyRNK0Ie"

# 直播空间名称
hubName = "derya"

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
