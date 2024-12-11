# 使用 Python 官方基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将代码和依赖文件拷贝到容器
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 的默认端口
EXPOSE 5000

# 启动命令
CMD ["source", ".env"]
CMD ["python", "app.py"]
