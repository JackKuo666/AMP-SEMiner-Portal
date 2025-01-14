import requests

def fetch_amps(records_per_page=10, page=1, source="", amp="", amplenmin=1, amplenmax=150, proClst80=None, sort_prop="ProID", sort_order="asc", tables="all_amp_protein_animal"):
    # 定义 API URL
    url = "http://127.0.0.1:5000/api/getAllAmps"

    # 设置查询参数
    params = {
        'records_per_page': records_per_page,  # 每页记录数
        'page': page,                           # 当前页数
        'source': source,                       # 源的过滤条件
        'amp': amp,                             # AMP的过滤条件
        'amplenmin': amplenmin,                 # AMP长度最小值
        'amplenmax': amplenmax,                 # AMP长度最大值
        'proClst80': proClst80,                 # Pro_clst80的过滤条件
        'sortProp': sort_prop,                  # 添加排序字段
        'sortOrder': sort_order,                # 添加排序方向
        'tables': tables                        # 指定查询的表
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)

        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            if data:
                total_count = data.get("total", 0)  # 获取总记录数
                results = data.get("data", [])  # 获取数据列表
                
                print(f"Total Count: {total_count}")  # 打印总记录数
                print("Received Data:", len(results))  # 打印接收到的数据条数
                for item in results:  # 遍历并打印每一项
                    print(item)
            else:
                print("No data returned.")
        else:
            print(f"Error: Received status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error while connecting to API: {e}")

# 测试 1: 获取第一页，每页 10 条记录，按 ProID 排序
print("Test 1")
fetch_amps(records_per_page=10, page=1, sort_prop="ProID", sort_order="asc")

# 测试 2: 获取第二页，并按名称过滤
print("\nTest 2")
fetch_amps(records_per_page=10, page=2, source="data_Hadza", sort_prop="AMPlen", sort_order="desc")

# 测试 3: 获取 human_gut_amps 表的数据，第一页，每页 5 条记录，按 AMP 名称排序
print("\nTest 3")
fetch_amps(records_per_page=5, page=1, tables="human_gut_amps", sort_prop="AMP", sort_order="asc")
