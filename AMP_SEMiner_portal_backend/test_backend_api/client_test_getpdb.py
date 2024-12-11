import requests

def fetch_pdb_file(file_path):
    # 定义 API URL
    url = "http://127.0.0.1:5000/api/getPdbFile"

    # 设置查询参数
    params = {
        'filePath': file_path  # 指定 PDB 文件的相对路径
    }

    try:
        # 发送 GET 请求获取 PDB 文件
        response = requests.get(url, params=params)

        # 检查响应状态码
        if response.status_code == 200:
            # 假设返回的是文件内容，保存到本地
            file_name = file_path.split('/')[-1]  # 获取文件名
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"File saved as {file_name}")
        else:
            print(f"Error: Received status code {response.status_code} for file path: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error while connecting to API: {e}")

# 测试 1: 请求并保存 PDB 文件
fetch_pdb_file('/mnt/asustor/wenhui.li/02.AMP/structure/AFstr/AMP_clst_btch3/C224992_relaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb')
