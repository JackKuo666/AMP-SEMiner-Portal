import requests

# 目标 API URL（修改为实际的服务器地址）
url = "http://localhost:5000/api/getProStruProperties"

# 查询参数
params = {
    'protein_id': 'C000037'
}

# 发送 GET 请求到后端 API
response = requests.get(url, params=params)

# 检查响应状态码
if response.status_code == 200:
    # 成功时打印返回的 JSON 数据
    data = response.json()
    print("Response data:", data)
else:
    # 失败时打印错误信息
    print(f"Error: {response.status_code}, {response.text}")
