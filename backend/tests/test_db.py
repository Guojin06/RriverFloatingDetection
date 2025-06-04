import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#添加项目根目录到Python路径，确保可以导入config.database
#sys是系统相关的模块，path是路径相关的模块，append是添加到列表的函数，os是操作系统相关的模块
from config.database import engine, Base
from sqlalchemy import text

def test_database_connection():
    try:
        # 测试数据库连接
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("数据库连接成功！")
            
            # 测试数据库版本
            version = connection.execute(text("SELECT VERSION()")).scalar()
            print(f"MySQL版本: {version}")
            
            # 测试数据库列表
            databases = connection.execute(text("SHOW DATABASES")).fetchall()
            print("\n可用的数据库:")
            for db in databases:
                print(f"- {db[0]}")
                
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")

if __name__ == "__main__":
    test_database_connection() 