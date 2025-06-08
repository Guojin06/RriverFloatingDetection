import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from config.database import engine

def test_connection():
    try:
        # 尝试执行一个简单的查询
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("数据库连接成功！")
            print(f"查询结果: {result.scalar()}")
            
            # 测试数据库版本
            version = connection.execute(text("SELECT VERSION()")).scalar()
            print(f"MySQL版本: {version}")
            
            # 测试用户权限
            user = connection.execute(text("SELECT CURRENT_USER()")).scalar()
            print(f"当前用户: {user}")
            
    except Exception as e:
        print("数据库连接失败！")
        print(f"错误信息: {str(e)}")

if __name__ == "__main__":
    test_connection() 