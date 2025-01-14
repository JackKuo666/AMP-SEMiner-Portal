FROM nginx:latest

# 删除默认的 Nginx HTML 文件
RUN rm -rf /usr/share/nginx/html/*

# 将本地的前端打包文件复制到 Nginx 镜像中
COPY dist /usr/share/nginx/html

# 复制自定义 Nginx 配置文件
COPY AMP_SEMiner_portal_frontend.conf /etc/nginx/conf.d/default.conf
