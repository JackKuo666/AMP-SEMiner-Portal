from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS
import mysql.connector
import os 
from oss2.credentials import EnvironmentVariableCredentialsProvider
from oss2 import ProviderAuthV4, Bucket
import requests
from functools import lru_cache
import json


app = Flask(__name__)
CORS(app)

# 数据库配置
db_config = {
    'user': os.environ.get('DB_USER'), 
    'password': os.environ.get('DB_PASSWORD'),  
    'host': os.environ.get('DB_HOST'),  
    'database': os.environ.get('DB_NAME'),  
}

bucket_config = {
    "endpoint": os.environ.get("OSS_ENDPOINT"),
    "region": os.environ.get("OSS_REGION"),
    "bucket_name": os.environ.get("OSS_BUCKET_NAME"),
}

pdb_folder_path = os.environ.get('PDB_FOLDER_PATH'), 

# 将缓存大小设置为 128，具体大小可根据需求调整
@lru_cache(maxsize=128)
def get_cached_query(query, params):
    """通过 lru_cache 缓存查询结果"""
    cursor = None
    conn = None
    try:
        # 建立数据库连接
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 执行查询
        cursor.execute(query, params)
        print(f"Executing query: {cursor.statement}")
        results = cursor.fetchall()

        # 返回 JSON 形式的结果
        return json.dumps(results)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return json.dumps({"error": str(err)})

    finally:
        # 确保关闭数据库连接
        cursor.close()
        conn.close()

@app.route('/api/getAllAmps', methods=['GET'])
def get_all_amps():
    try:
        # 获取 URL 查询参数
        records_per_page = request.args.get('records_per_page', default=10, type=int)
        tables = request.args.get('tables', default="all_amp_protein_animal", type=str)
        page = request.args.get('page', default=1, type=int)
        amplenmin = request.args.get('amplenmin', default=1, type=int)
        amplenmax = request.args.get('amplenmax', default=500, type=int)
        proClst80 = request.args.get('proClst80', default=None, type=int)
        ampClst = request.args.get('ampClst', default=None, type=int)
        source = request.args.get('source', default=None, type=str)
        ProID = request.args.get('proID', default=None, type=str)
        Position = request.args.get('position', default=None, type=str)
        amp_same = request.args.get('amp_same', default=None, type=int)
        amp = request.args.get('amp', default=None, type=str)
        sort_prop = request.args.get('sortProp', default='ProID', type=str)
        sort_order = request.args.get('sortOrder', default='asc', type=str)

        # SQL 动态生成
        count_query = f"SELECT COUNT(*) AS total_count FROM {tables} WHERE 1=1"
        data_query = f"SELECT * FROM {tables} WHERE 1=1"
        params = []

        # 添加过滤条件
        if source:
            count_query += " AND Source = %s"
            data_query += " AND Source = %s"
            params.append(f"{source}")
        if amp_same is None:
            if amp:
                # 因为fulltext索引的限制，如果搜索词少于5个字符，使用LIKE，否则使用全文搜索
                if len(amp) < 5:
                    count_query += " AND AMP LIKE %s"
                    data_query += " AND AMP LIKE %s"
                    params.append(f"%{amp}%")
                else:
                    count_query += " AND MATCH(AMP) AGAINST (%s IN NATURAL LANGUAGE MODE)"
                    data_query += " AND MATCH(AMP) AGAINST (%s IN NATURAL LANGUAGE MODE)"
                    params.append(f"{amp}")
        else:
            if amp:
                count_query += " AND AMP = %s"
                data_query += " AND AMP = %s"
                params.append(amp)
        if amplenmin != 1:
            count_query += " AND AMPlen >= %s"
            data_query += " AND AMPlen >= %s"
            params.append(amplenmin)
        if amplenmax != 500:
            count_query += " AND AMPlen <= %s"
            data_query += " AND AMPlen <= %s"
            params.append(amplenmax)
        if proClst80 is not None:
            count_query += " AND Pro_clst80 = %s"
            data_query += " AND Pro_clst80 = %s"
            params.append(proClst80)
        if ampClst is not None:
            count_query += " AND AMP_clst = %s"
            data_query += " AND AMP_clst = %s"
            params.append(ampClst)
        if ProID:
            count_query += " AND ProID = %s"
            data_query += " AND ProID = %s"
            params.append(ProID)
        if Position:
            count_query += " AND Position = %s"
            data_query += " AND Position = %s"
            params.append(Position)

        # 添加排序和分页
        valid_sort_props = ['ProID', 'AMP', 'AMPlen', 'Source', 'Pro_clst80', 'AMP_clst']
        if sort_prop in valid_sort_props:
            data_query += f" ORDER BY {sort_prop} {sort_order.upper()}"
        offset = (page - 1) * records_per_page
        data_query += " LIMIT %s OFFSET %s"
        params.extend([records_per_page, offset])

        # 获取缓存结果
        total_count = json.loads(get_cached_query(count_query, tuple(params[:len(params) - 2])))[0]['total_count']
        results = json.loads(get_cached_query(data_query, tuple(params)))

        # 返回 JSON 响应
        return jsonify({"total": total_count, "data": results})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/getPdbFile', methods=['GET'])
def get_pdb_file():
    # try:
    # 获取传入的文件路径（通过查询参数传递）
    file_path = request.args.get('filePath')
    print("file path", file_path)

    file_path = os.path.join(pdb_folder_path[0], str(file_path))

    if not file_path:
        return jsonify({"error": "filePath parameter is required"}), 400
                    
    auth = ProviderAuthV4(EnvironmentVariableCredentialsProvider())
    bucket = Bucket(auth, **bucket_config)

    
    # 生成签名URL
    url = bucket.sign_url('GET', file_path, 600, slash_safe=True)
    print("Generated signed URL:", url)

    # 发起HTTP请求以获取文件内容
    response = requests.get(url, stream=True)
    print("Response status code:", response.status_code)

    if response.status_code == 200:
        # 返回文件内容
        return Response(
            response.iter_content(chunk_size=8192),
            content_type='chemical/x-pdb',
            headers={
                'Content-Disposition': f"attachment; filename=\"{file_path.split('/')[-1]}\""
            }
        )
    else:
        return jsonify({"error": f"Failed to fetch file. HTTP status code: {response.status_code}"}), 500

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


@app.route('/api/getSeqProperties', methods=['GET'])
def get_seq_properties():
    cursor = None
    conn = None
    try:
        # 获取 URL 查询参数
        amp = request.args.get('amp', default='', type=str)

        # 打印查询参数
        print(f"Query parameters - amp: {amp}")

        # 连接到数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 执行查询
        query = "SELECT * FROM SeqProperties WHERE AMP = %s"
        cursor.execute(query, (amp,))

        # 获取查询结果
        results = cursor.fetchall()

        # 返回数据的 JSON 响应
        return jsonify({"data": results})

    except mysql.connector.Error as err:
        # 打印错误日志
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/getProStruProperties', methods=['GET'])
def get_pro_stru_properties():
    cursor = None
    conn = None
    try:
        # 获取 URL 查询参数
        protein_id = request.args.get('protein_id', default=None, type=str)
        
        # 打印查询参数
        print(f"Query parameter - protein_id: {protein_id}")

        if not protein_id:
            return jsonify({"error": "ProteinID is required"}), 400

        # 连接到数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 查询语句
        query = "SELECT * FROM Pro_StruProperties WHERE ProteinID = %s"
        cursor.execute(query, (protein_id,))
         # 获取查询结果
        results = cursor.fetchall()

        if results:
            return jsonify({"data": results})
        else:
            return jsonify({"error": "ProteinID not found"}), 404

    except mysql.connector.Error as err:
        # 打印错误日志
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/getStruProperties', methods=['GET'])
def get_stru_properties():
    cursor = None
    conn = None
    try:
        protein_id = request.args.get('protein_id', default='', type=str)
        
        # 构建查询条件
        query = "SELECT * FROM StruProperties WHERE ProteinID LIKE %s"
        params = [f"%{protein_id}%"]

        # 连接数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 执行查询
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        # 返回数据
        return jsonify({"data": results})

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
