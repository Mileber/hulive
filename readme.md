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

