# Vue 3 + Vite
# 1.use npm run preview 运行

### 0.项目根目录下新建.env文件

```angular2html
VITE_BASE_API_prod=http://127.0.0.1:5000/api # 线上环境
VITE_MOCK_API_prod=api                       # 本地模拟数据                       
VITE_BASE_API_dev=http://127.0.0.1:5000/api  # 开发环境
VITE_MOCK_API_dev=api                        # 本地模拟数据
```

### 1. **确保安装依赖**
在项目的根目录下，确保你已经安装了所有的依赖包。运行以下命令来安装：
```bash
node -v
v20.18.0
```
如果不是，需要用nvm管理node
```bash
nvm ls
nvm use v20.18.0
```

```bash
npm install
```

### 2. **运行开发服务器**
运行以下命令启动开发服务器：
```bash
npm run dev
```

这将执行 `package.json` 文件中定义的 `dev` 脚本。通常情况下，这会启动一个本地的开发服务器（如 Webpack Dev Server、Vite、Next.js 等），并监听你项目中的源代码文件。一旦你做出修改，开发服务器通常会自动重新加载页面。

### 3. **访问开发环境**
开发服务器通常会启动在本地某个端口上（常见的是 `localhost:5173` ），你可以在浏览器中输入相应地址访问你的应用。

- 如果开发服务器运行在 `localhost:5173`，那么你可以在浏览器地址栏输入：
  ```
  http://localhost:5173
  ```

具体的端口号可以在命令行中看到，或者在 `package.json` 中查看 `dev` 脚本的配置。

### 4. **构建生产环境**

```angular2html
npm run dev
npm run build
npm run preview
```

# 2.docker 运行
将前端资源编译打包并交付给平台基建组，主要涉及以下步骤：

---

### **1. 编译和打包前端资源**

1. **构建项目**：
   使用 `npm run build` 命令生成静态资源：
   ```bash
   npm run build
   ```
   这会在项目根目录下生成一个 `dist` 文件夹，包含所有的静态文件。

2. **检查打包结果**：
   确保 `dist` 文件夹中的内容是完整的，包括 `index.html` 和相关的 CSS、JS 文件。

---

### **2. 配置 Nginx**

#### **2.1 创建 Nginx 配置文件**
为前端项目配置 Nginx。新建一个 Nginx 配置文件，例如 `my-vue-app.conf`，内容如下：

```nginx
server {
    listen 80;
    server_name mag-ampome.aigene.org.cn; # 替换为实际的域名或 IP 地址

    root /usr/share/nginx/html; # 指定静态资源的路径
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    error_page 404 /index.html;

    # 可选：配置 gzip 压缩
    gzip on;
    gzip_types text/plain application/javascript text/css application/json;
}
```

#### **2.2 确保目录一致**
在配置文件中，`root` 指定的路径是 Nginx 用来加载前端资源的目录。比如 `/usr/share/nginx/html`。

---

### **3. 将前端资源放入 Nginx 镜像**

1. **创建 Dockerfile**
   在项目目录下新建一个 `Dockerfile` 文件：
   ```dockerfile
   FROM nginx:latest

   # 删除默认的 Nginx HTML 文件
   RUN rm -rf /usr/share/nginx/html/*

   # 将本地的前端打包文件复制到 Nginx 镜像中
   COPY dist /usr/share/nginx/html

   # 复制自定义 Nginx 配置文件
   COPY AMP_SEMiner_portal_frontend.conf /etc/nginx/conf.d/default.conf
   ```

2. **构建镜像**
   使用 Docker 构建 Nginx 镜像：
   ```bash
   docker build -t amp_seminer_portal_frontend-nginx .
   ```

3. **验证镜像**
   运行生成的 Docker 镜像以验证配置是否正确：
   ```bash
   docker run -p 8080:80 amp_seminer_portal_frontend-nginx
   ```
   在浏览器中访问 `http://localhost:8080`，检查是否能够正确加载前端页面。

---

### **4. 将镜像交付给平台基建组**

1. **标记镜像**
   给镜像打标签，指向公司或团队的 Docker Registry：
   ```bash
   docker tag amp_seminer_portal_frontend-nginx jackkuo666/amp_seminer_portal_frontend-nginx:v2
   ```

2. **推送镜像**
   将镜像推送到指定的 Docker Registry：
   ```bash
   docker push jackkuo666/amp_seminer_portal_frontend-nginx:v2
   ```

3. **通知基建组**
   向平台基建组提供以下信息：
  - 镜像名称和版本（例如：`jackkuo666/amp_seminer_portal_frontend-nginx:v2`）。
  - 配置中使用的端口（默认 80）。
  - 依赖的环境变量或运行时配置（如果有）。

---

### **5. 平台基建组的操作建议**

基建组拉取镜像后，可以使用以下命令部署镜像：
```bash
docker pull jackkuo666/amp_seminer_portal_frontend-nginx:v2
docker run -d -p 80:80 --name amp_seminer_portal_frontend-nginx jackkuo666/amp_seminer_portal_frontend-nginx:v2
```

如果在 Kubernetes 环境下运行，建议基建组编写一个 Deployment 和 Service 配置文件，以便进行集群内的部署。

---

### **6. 总结**
- **前端开发者**：负责编译、配置 Nginx、构建 Docker 镜像并推送到 Registry。
- **基建组**：拉取镜像并部署到目标环境。

通过这种方式，前端项目可以高效地交付和运行在生产环境中。