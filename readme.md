# 环境配置
1. pip install Flask
2. pip install flask-sqlalchemy
3. pip install pili2

# 提示码
- 正确时返回完整 json 格式数据，错误时返回相关错误码
- 101 : 正确码
- 501 : 未找到
- 502 : 密码错误


# 数据库说明
## 1. User表
| Field      | Type        | Null | Key | Default | Extra          |
------------ | ------------- | ------| ----- | --------- | ---------------- |
| id         | int(11)     | NO   | PRI | NULL    | auto_increment |
| name       | varchar(20) | NO   | UNI | NULL    |                |
| password   | varchar(50) | NO   |     | NULL    |                |
| phone      | varchar(15) | YES  | UNI | NULL    |                |
| stream_key | varchar(50) | YES  | UNI | NULL    |                |


## 2. Stream表 
| Field      | Type        | Null | Key | Default | Extra |
|------------|-------------|------|-----|---------|-------|
| stream_key | varchar(50) | NO   | PRI | NULL    |       |
| title      | varchar(50) | YES  |     | NULL    |       |
| level      | int(11)     | NO   |     | NULL    |       |

