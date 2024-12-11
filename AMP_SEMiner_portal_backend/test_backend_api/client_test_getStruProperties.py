import requests

# API 服务器地址
api_url = "http://localhost:5000/api/getStruProperties"

# 要查询的蛋白质 ID 0|90|236|C224992:35-45
protein_id = "134387|162|8693|C288763:219-223"  # 替换成你要查询的蛋白质 ID
protein_id = "0|90|236|C224992:35-45"  # 替换成你要查询的蛋白质 ID

# 发送 GET 请求
response = requests.get(api_url, params={"protein_id": protein_id})

# 检查响应状态
if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        print("Query Results:")
        for row in data['data']:
            print(row)  # 打印每一行数据
    elif 'error' in data:
        print(f"Error: {data['error']}")
else:
    print(f"Request failed with status code: {response.status_code}")
