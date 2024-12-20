# optional, use aliyun oss to store pdb data
first, you shloud install aliyun oss client
```
pip install oss2
```
and set your aliyun oss access key and secret key
```python
OSS_ACCESS_KEY_ID=xxx
OSS_ACCESS_KEY_SECRET=yyy
```

## 1. upload pdb data to aliyun oss
[up_pdb_to_oss.py](up_pdb_to_oss.py)
## 2. get oss pdb example code
[get_oss_pdb.py](get_oss_pdb.py)