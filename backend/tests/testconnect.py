import pymysql
conn = pymysql.connect(
    host="10.201.120.113",
    port=3306,
    user="remote_user",
    password="123456",
    database="river_floating_detection"
)
print("连接成功！")