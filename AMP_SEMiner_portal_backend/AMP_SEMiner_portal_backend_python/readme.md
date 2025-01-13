# mysql data preparation
## 1. Install mysql
```
sudo apt-get install mysql-server
```
## 2. Load the already created table
```
mysql -u root -p
```
need [amps_backup.sql](amps_backup.sql)into `AMP_SEMiner_portal_backend_docker/amps_backup.sql`
```sql
CREATE DATABASE amps;
mysql -u root -p amps < ../AMP_SEMiner_portal_backend_docker/amps_backup.sql
```
Verify it:
```sql
select * from human_gut_amps limit 2;
```
Start mysql service
```
sudo systemctl start mysql
```

Some other commands that may be useful:
Restart mysql service
```
sudo systemctl restart mysql
```
Close mysql service
```
sudo systemctl stop mysql
```
View mysql service status
```
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
pdb_folder_path={your/pdb/folder/path} 
```

# 4.Run
```
python app.py
```