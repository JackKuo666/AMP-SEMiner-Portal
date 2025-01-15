# Vue 3 + Vite  
### 1. Run with `npm run preview`

### 0. Create a `.env` file in the current directory

```angular2html
VITE_BASE_API_prod=https://amp-seminer.gateway.aigene.org.cn/api  # Production environment
VITE_MOCK_API_prod=api                       # Local mock data
VITE_BASE_API_dev=http://127.0.0.1:5000/api  # Development environment
VITE_MOCK_API_dev=api                        # Local mock data
```

### 1. **Ensure dependencies are installed**  
Make sure you have installed all the required dependencies in the root directory of the project. Run the following commands to check and install:

```bash
node -v
v20.18.0
```

If the version is incorrect, use `nvm` to manage your Node.js version:
```bash
nvm ls
nvm use v20.18.0
```

Then, install the dependencies:
```bash
npm install
```

### 2. **Run the development server**  
Run the following command to start the development server:

```bash
npm run dev
```

This will execute the `dev` script defined in the `package.json` file. Typically, this will start a local development server (such as Webpack Dev Server, Vite, Next.js, etc.) and listen for changes in your source code. Once you make changes, the development server will automatically reload the page.

### 3. **Access the development environment**  
The development server typically runs on a local port (commonly `localhost:5173`), and you can access the application by navigating to that address in your browser.

- If the server is running on `localhost:5173`, enter the following URL in the browser:
  ```
  http://localhost:5173
  ```

You can find the exact port number in the terminal output or check the `dev` script configuration in `package.json`.

### 4. **Build for production**  
Run the following commands to build and preview the application for production:

```bash
npm run build
npm run preview
```

---

# 2. Docker Deployment  
To deliver the packaged frontend resources to the platform infrastructure team, follow these steps:

---

### **1. Compile and Package Frontend Resources**

1. **Build the project**  
   Use the `npm run build` command to generate the static resources:

   ```bash
   npm run build
   ```

   This will create a `dist` folder in the root directory containing all the static files.

2. **Verify the build**  
   Ensure that the `dist` folder contains all necessary files, including `index.html` and the related CSS and JS files.

---

### **2. Configure Nginx**

#### **2.1 Create the Nginx configuration file**  
Configure Nginx for the frontend project. Create a new Nginx configuration file, such as `my-vue-app.conf`, with the following content:

```nginx
server {
    listen 80;
    server_name mag-ampome.aigene.org.cn; # Replace with actual domain or IP address

    root /usr/share/nginx/html; # Path for static resources
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    error_page 404 /index.html;

    # Optional: Enable gzip compression
    gzip on;
    gzip_types text/plain application/javascript text/css application/json;
}
```

#### **2.2 Ensure directory consistency**  
In the configuration file, the `root` path specifies the directory where Nginx will load the frontend resources. For example, `/usr/share/nginx/html`.

---

### **3. Place Frontend Resources into the Nginx Image**

1. **Create a Dockerfile**  
   In the project directory, create a `Dockerfile`:

   ```dockerfile
   FROM nginx:latest

   # Remove the default Nginx HTML files
   RUN rm -rf /usr/share/nginx/html/*

   # Copy the local frontend build files to the Nginx image
   COPY dist /usr/share/nginx/html

   # Copy the custom Nginx config file
   COPY AMP_SEMiner_portal_frontend.conf /etc/nginx/conf.d/default.conf
   ```

2. **Build the image**  
   Use Docker to build the Nginx image:

   ```bash
   npm run build
   docker build -t amp_seminer_portal_frontend-nginx .
   ```

3. **Verify the image**  
   Run the generated Docker image to verify that the configuration is correct:

   ```bash
   docker run -p 8080:80 amp_seminer_portal_frontend-nginx
   ```

   In your browser, visit `http://localhost:8080` and check if the frontend page loads correctly.

---

### **4. Deliver the Image to the Platform Infrastructure Team**

1. **Tag the image**  
   Tag the image to point to your company's Docker registry:

   ```bash
   docker tag amp_seminer_portal_frontend-nginx jackkuo666/amp_seminer_portal_frontend-nginx:v2
   ```

2. **Push the image**  
   Push the image to the specified Docker registry:

   ```bash
   docker push jackkuo666/amp_seminer_portal_frontend-nginx:v2
   ```

3. **Notify the infrastructure team**  
   Provide the platform infrastructure team with the following information:
   - Image name and version (e.g., `jackkuo666/amp_seminer_portal_frontend-nginx:v2`).
   - Ports used in the configuration (default: 80).
   - Any required environment variables or runtime configurations (if any).

---

### **5. Infrastructure Team's Actions**

After the infrastructure team pulls the image, they can deploy it with the following commands:

```bash
docker pull jackkuo666/amp_seminer_portal_frontend-nginx:v2
docker run -d -p 80:80 --name amp_seminer_portal_frontend-nginx jackkuo666/amp_seminer_portal_frontend-nginx:v2
```

If running in a Kubernetes environment, the infrastructure team should write a Deployment and Service configuration file for deployment within the cluster.

---

### **6. Summary**

- **Frontend Developers**: Responsible for compiling, configuring Nginx, building Docker images, and pushing them to the registry.
- **Infrastructure Team**: Pulls the image and deploys it in the target environment.

This approach ensures that the frontend project is efficiently delivered and runs in a production environment.

---
