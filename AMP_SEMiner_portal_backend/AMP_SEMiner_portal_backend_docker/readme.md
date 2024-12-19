# 1. Install Docker Compose
```
sudo apt-get install docker-compose

```

# 2.set environment to .env
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
sudo docker-compose up --build
```
Stop service:
```bash
sudo docker-compose down
```

Other commands:

Execute the following command to delete useless resources in Docker, including unused images, containers, networks, and volumes:
```bash
sudo docker system prune -a
```
This command will delete the following:

stopped container

Image not used by any container

unused network

unused volume