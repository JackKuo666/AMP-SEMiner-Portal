import requests

def test_get_pdb_file():
    # Flask 服务地址
    base_url = "http://127.0.0.1:5000/api/getPdbFile"

    # 测试的文件路径（替换为实际文件路径）
    file_path = "AMP-SEMiner/AMP_fragment_pdbs/0|1150|38060|C000004:21-31.pdb"

    # 发送请求
    try:
        response = requests.get(base_url, params={"filePath": file_path}, stream=True)

        # 打印状态码
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            # 保存下载的文件
            output_file = file_path.split('/')[-1]
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"File downloaded successfully as {output_file}")
        else:
            print(f"Error: {response.json()}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_get_pdb_file()
