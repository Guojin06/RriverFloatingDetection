
chcp 65001
echo ===================================
echo 开始启动后端服务...
echo ===================================

echo 检查Python环境...
set PYTHON_PATH=C:\Python\Python312\python.exe
if not exist "%PYTHON_PATH%" (
    echo 错误: 未找到Python解释器，请确认路径: C:\Python\Python312\python.exe
    pause
    exit /b 1
)

echo 检查Python版本...
"%PYTHON_PATH%" --version

echo 启动服务器...
echo 如果长时间无响应，请检查:
echo 1. 端口9000是否被占用
echo 2. 数据库是否正常运行
echo 3. 模型文件是否正确
echo ===================================
"%PYTHON_PATH%" -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload

