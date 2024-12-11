# -*- coding: utf-8 -*-
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice


# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = "https://oss-cn-hangzhou.aliyuncs.com"

# 填写Endpoint对应的Region信息，例如cn-hangzhou。注意，v4签名下，必须填写该参数
region = "cn-hangzhou"

# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, endpoint, "lscp-tools-data", region=region)

# 列举Bucket下的10个文件。
for b in islice(oss2.ObjectIterator(bucket), 10):
    print(b.key)


# 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。
object_name = 'AMP-SEMiner/AMP_fragment_pdbs/0|1150|38060|C000004:21-31.pdb'

# 指定HTTP查询参数。
params = dict()
# 设置单链接限速，单位为bit，例如限速100 KB/s。
# params['x-oss-traffic-limit'] = str(100 * 1024 * 8)
# 指定IP地址或者IP地址段。
# params['x-oss-ac-source-ip'] = "127.0.0.1"
# 指定子网掩码中1的个数。
# params['x-oss-ac-subnet-mask'] = "32"
# 指定VPC ID。
# params['x-oss-ac-vpc-id'] = "vpc-t4nlw426y44rd3iq4xxxx"
# 指定是否允许转发请求。
# params['x-oss-ac-forward-allow'] = "true"

# 生成下载文件的签名URL，有效时间为60秒。
# 生成签名URL时，OSS默认会对Object完整路径中的正斜线（/）进行转义，从而导致生成的签名URL无法直接使用。
# 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
url = bucket.sign_url('GET', object_name, 600, slash_safe=True, params=params)
print('签名URL的地址为：', url)