import pymysql
import ast
import json

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="river_floating_detection",
    charset="utf8mb4"
)
cursor = conn.cursor()

cursor.execute("SELECT id, result_json FROM detection_results")
for id, result_json in cursor.fetchall():
    if result_json and result_json.strip().startswith('['):
        try:
            # 用 ast.literal_eval 解析 Python 字符串
            py_obj = ast.literal_eval(result_json)
            # 转为标准 JSON 字符串
            json_str = json.dumps(py_obj, ensure_ascii=False)
            # 更新数据库
            cursor.execute("UPDATE detection_results SET result_json=%s WHERE id=%s", (json_str, id))
        except Exception as e:
            print(f"修正失败 id={id}: {e}")

conn.commit()
cursor.close()
conn.close()
print("修正完成！")