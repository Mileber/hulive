# 用户相关

1. 插入
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/liveUser/userInsert/' -d '{"id":"0", "name":"HongkongTv", "password":"hk", "stream_key":"0", "phone":"0"}'

2. 查询
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/userQuery/' -d '{ "id":2}'

3. 更新用户
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/userUpdate/' -d '{"id":1, "name":"hhhhh", "password":"123456", "stream_key":"15021057217", "phone":"15021057217"}'

# 直播表相关

1. 插入
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/liveInfo/streamInsert/' -d '{"stream_key":"15021057217", "title":"hhhh", "level":1}'

2. 更新
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/streamUpdate/' -d '{"stream_key":"15021057217", "title":"233333", "level":1}'
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/streamUpdate/' -d '{"stream_key":"15021057217", "title":"233333", "level":5}'

3. 查询
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/streamQuery/' -d '{ "stream_key":"15021057217"}'

# follow表相关

1. 查询关注列表及人数
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/huli/getFollowList/' -d '{ "user_id":8}'

2. 新增关注
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/huli/insertFollow/' -d '{ "from_id":8, "to_id":9}'

# 直播流相关

1. 生成带授权凭证的 RTMP 推流地址
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/huli/getRTMPPublishURL/' -d '{ "key":"test"}'

2. 生成 RTMP 播放地址
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getRTMPPlayURL/' -d '{ "key":"15021057217"}'

3. 生成 HLS 播放地址
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getHLSPlayURL/' -d '{ "key":"15021057217"}'

4. 生成 HDL(HTTP-FLV) 播放地址
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getHDLPlayURL/' -d '{ "key":"15021057217"}'

5. 生成直播封面地址
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/huli/getSnapshotPlayURL/' -d '{ "key":"test"}'

6. 创建流
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/huli/createStream/' -d '{ "key":"test"}'

7. 获得流
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getStream/' -d '{ "key":"15021057217"}'

8. 查询流列表
curl -i -H "Content-Type: application/json" -X POST 'http://pearapple.net:8001/huli/getStreamList/' -d '{ }'

*9. 查询直播列表*

10. 查询流信息
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getStreamInfo/' -d '{ "key":"15021057217"}'

11. 禁播流
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/disableStream/' -d '{ "key":"15021057217", "time":"5"}'

12. 启用流
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/enableStream/' -d '{ "key":"15021057217"}'

13. 查询直播实时信息
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getLiveStatus/' -d '{ "key":"15021057217"}'

14. 保存直播回放
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/Save/' -d '{ "key":"15021057217"}'

15. 查询直播历史记录
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/getHistoryActivity/' -d '{ "key":"15021057217"}'

*16. 开始*
curl -i -H "Content-Type: application/json" -X POST 'http://localhost:5000/huli/start/' -d '{ "key":"15021057217"}'