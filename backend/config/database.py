from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os#os模块用于获取环境变量

# 加载环境变量
load_dotenv()#加载环境变量,从.env文件中获取

# 数据库连接配置
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/river_floating_detection?charset=utf8mb4"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 自动处理断开的连接
    pool_recycle=3600,   # 连接回收时间
    echo=True            # 打印SQL语句（开发环境使用）
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("MYSQL_USER:", SQLALCHEMY_DATABASE_URL)
print("MYSQL_PASSWORD:", SQLALCHEMY_DATABASE_URL)
print("MYSQL_HOST:", SQLALCHEMY_DATABASE_URL)
print("MYSQL_PORT:", SQLALCHEMY_DATABASE_URL)
print("MYSQL_DATABASE:", SQLALCHEMY_DATABASE_URL) 