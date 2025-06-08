from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os#os模块用于获取环境变量

# 加载环境变量
load_dotenv()#加载环境变量,从.env文件中获取

# 数据库配置（使用远程MySQL配置）
MYSQL_USER = os.getenv("MYSQL_USER", "remote_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")  
MYSQL_HOST = os.getenv("MYSQL_HOST", "10.201.120.113")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "river_floating_detection")#数据库名称，getenv获取环境变量

# 创建数据库URL（使用pymysql作为驱动）
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 自动处理断开的连接
    pool_recycle=600,   # 缩短回收连接时间
    echo=True,           # 打印SQL语句（开发环境使用）
    pool_size=2,         # 连接池大小
    max_overflow=5      # 最大溢出连接数
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

print("MYSQL_USER:", MYSQL_USER)
print("MYSQL_PASSWORD:", MYSQL_PASSWORD)
print("MYSQL_HOST:", MYSQL_HOST)
print("MYSQL_PORT:", MYSQL_PORT)
print("MYSQL_DATABASE:", MYSQL_DATABASE) 