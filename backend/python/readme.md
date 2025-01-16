# AMP_SEMiner_portal_backend_python
This folder contains the backend code, and Docker is not required. You can simply install the Python dependencies and import the SQL file to run the application.

# 1.mysql data preparation
## 1. Install mysql
```sh
sudo apt-get install mysql-server
```
## 2. Load the already created table
need download [amps_backup.sql](https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/amps_backup.sql)into Current folder 

```sh
mysql -u root -p
```

```sql
CREATE DATABASE amps;
```

```sh
mysql -u root -p amps < ./amps_backup.sql
```

```sh
mysql -u root -p
```

```sql

mysql> use amps;

Database changed
mysql> show tables;
+------------------------+
| Tables_in_amps         |
+------------------------+
| Pro_StruProperties     |
| SeqProperties          |
| StruProperties         |
| all_amp_protein_animal |
| human_gut_amps         |
+------------------------+
```

Verify it:
```sql
select * from human_gut_amps limit 2;
```

Start mysql service
```sh
sudo systemctl start mysql
```

Some other commands that may be useful:
Restart mysql service
```sh
sudo systemctl restart mysql
```
Close mysql service
```sh
sudo systemctl stop mysql
```
View mysql service status
```sh
sudo systemctl status mysql
```


Of course, you can also build through [raw data](../data_source/Build%20mysql%20from%20raw%20data%20optional.md), but you need to manually build the table structure yourself. Only the tables that have been built are provided here.

# 2. Install python environment
```
python 3.9
```
```
pip install -r requirements.txt
```


# 3.set environment to .env
```
DB_USER={your_mysql_username}
DB_PASSWORD=2
DB_HOST=localhost
DB_NAME=amps
PDB_FOLDER_PATH={your/pdb/folder/path} 
```

# 4.Run
```
python app.py
```