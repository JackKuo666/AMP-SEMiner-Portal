# AMP_SEMiner_portal_backend_docker_build

This page is intended for developers. If you are a user of this project, please use the pre-built Docker images from a different directory: [AMP_SEMiner_portal_backend_docker_use](../AMP_SEMiner_portal_backend_docker_use).


As the backend of this project uses a MySQL database, two Docker images are used to run the application via Docker Compose.


The basic logic is as follows: You can first take a look at the [docker-compose.yml](docker-compose.yml) file, which contains two containers. One is `flask-app`, the backend code that needs to be built, and the other is the `official MySQL container`, using the image mysql:8.0.


So, from the line `- ./amps_backup.sql:/docker-entrypoint-initdb.d/amps_backup.sql` you can see that you need to manually download the data from [[amps_backup.sql](https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/amps_backup.sql)] and place it in the current folder to successfully load the MySQL container.


# 1. Install Docker Compose

```
sudo apt-get install docker-compose

```

# 2. Set the environment variables in the .env file located in the current folder.
```
DB_USER={your mysql username}
DB_PASSWORD=2
DB_ROOT_PASSWORD=rootpassword
DB_HOST=mysql
DB_NAME=amps
OSS_ACCESS_KEY_ID={your access key}
OSS_ACCESS_KEY_SECRET={your secret key}
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_REGION=cn-hangzhou
OSS_BUCKET_NAME=lscp-tools-data
pdb_folder_path=AMP-SEMiner/
```

# 3.Use Docker Compose

Start the service:
```bash
docker-compose up --build
```
now you can start service, look the port 5000, and in [test_backend_api](../../test_backend_api) `python client.py` to test port.

Stop service:
```bash
docker-compose down
```

# 3. push image to docker hub
build:
```sh
docker build -t jackkuo666/amp_seminer_portal_backend_flask:latest .
```
push:
```sh
docker push jackkuo666/amp_seminer_portal_backend_flask:latest
```

# Other commands:


Execute the following command to delete useless resources in Docker, including unused images, containers, networks, and volumes:
```bash
docker system prune -a
```
This command will delete the following:

stopped container

Image not used by any container

unused network

unused volume