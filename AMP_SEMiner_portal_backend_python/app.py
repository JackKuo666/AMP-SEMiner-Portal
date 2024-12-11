from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
db_config = {
    'user': os.environ.get('DB_USER'), 
    'password': os.environ.get('DB_PASSWORD'),  
    'host': os.environ.get('DB_HOST'),  
    'database': os.environ.get('DB_NAME'),  
}
pdb_folder_path = os.environ.get('pdb_folder_path'), 

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
        source = request.args.get('source', default='', type=str)
        ProID = request.args.get('proID', default='', type=str)
        Position = request.args.get('position', default='', type=str)
        amp_same = request.args.get('amp_same', default=None, type=int)
        amp = request.args.get('amp', default='', type=str)
        sort_prop = request.args.get('sortProp', default='ProID', type=str)  # 默认排序列
        sort_order = request.args.get('sortOrder', default='asc', type=str)  # 默认排序方向

        # 打印查询参数
        print(f"Query parameters - records_per_page: {records_per_page}, page: {page}, source: {source}, amplenmin: {amplenmin}, amplenmax: {amplenmax}, amp: {amp}, sortProp: {sort_prop}, sortOrder: {sort_order}")

        # 连接到数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 先查询总记录数
        if tables == "all_amp_protein_animal":
            count_query = "SELECT COUNT(*) AS total_count FROM all_amp_protein_animal WHERE 1=1"
        elif tables == "human_gut_amps":
            count_query  = "SELECT COUNT(*) AS total_count FROM human_gut_amps WHERE 1=1"
        else:
            print(f"tables error: {tables}")
            return jsonify({"error": "tables error"}), 400
        params = []  # 存储查询参数

        if tables == "all_amp_protein_animal":
            if source:
                count_query += " AND Source LIKE %s"
                params.append(f"%{source}%")  # 添加参数，用于模糊匹配
            if amp_same is None:                
                if  amp:
                    count_query += " AND AMP LIKE %s"
                    params.append(f"%{amp}%")  # 添加参数，用于模糊匹配
            else:
                if  amp:
                    count_query += " AND AMP = %s"
                    params.append(amp)  # 添加参数，用于模糊匹配
            if amplenmin is not None and amplenmin != 1:
                count_query += " AND AMPlen >= %s"
                params.append(amplenmin)
            if amplenmax is not None and amplenmax != 500:
                count_query += " AND AMPlen <= %s"
                params.append(amplenmax)
            if proClst80 is not None:
                count_query += " AND Pro_clst80 = %s"
                params.append(proClst80)
        elif tables == "human_gut_amps":
            if amp:
                count_query += " AND AMP = %s"
                params.append(amp)  
            if source:
                count_query += " AND Source = %s"
                params.append(source)  
            if ProID:
                count_query += " AND ProID = %s"
                params.append(ProID)  
            if Position:
                count_query += " AND Position = %s"
                params.append(Position)  



        # 执行查询
        cursor.execute(count_query, tuple(params))
        total_count = cursor.fetchone()['total_count']

        # 动态 SQL 查询
        if tables == "all_amp_protein_animal":
            query = "SELECT * FROM all_amp_protein_animal WHERE 1=1"
        elif tables == "human_gut_amps":
            query  = "SELECT * FROM human_gut_amps WHERE 1=1"
        else:
            print(f"tables error: {tables}")
            return jsonify({"error": "tables error"}), 400
        params = []

        if tables == "all_amp_protein_animal":
            if source:
                query += " AND Source LIKE %s"
                params.append(f"%{source}%")
            if amp_same is None:
                if amp:
                    query += " AND AMP LIKE %s"
                    params.append(f"%{amp}%")
            else:
                if amp:
                    query += " AND AMP = %s"
                    params.append(amp)
            if amplenmin is not None and amplenmin != 1:
                query += " AND AMPlen >= %s"
                params.append(amplenmin)
            if amplenmax is not None and amplenmax != 500:
                query += " AND AMPlen <= %s"
                params.append(amplenmax)
            if proClst80 is not None:
                query += " AND Pro_clst80 = %s"
                params.append(proClst80)
        elif tables == "human_gut_amps":
            if amp:
                query += " AND AMP = %s"
                params.append(amp)
            if source:
                query += " AND Source = %s"
                params.append(source)
            if ProID:
                query += " AND ProID = %s"
                params.append(ProID)
            if Position:
                query += " AND Position = %s"
                params.append(Position)

        
        if tables == "all_amp_protein_animal":
            # 添加排序逻辑
            valid_sort_props = ['ProID', 'AMP', 'AMPlen', 'Source', 
                                'Pro_clst80', 'Position', 'CID',
                                'AMP_clst','Sequence',
                                'KEGG_Pathway','seed_ortholog','GOs','KEGG_ko']  # 允许排序的字段
            if sort_prop in valid_sort_props:
                query += f" ORDER BY {sort_prop} {sort_order.upper()}"  # 使用 ORDER BY 子句

            # 分页逻辑
            if records_per_page > 0:
                offset = (page - 1) * records_per_page
                query += " LIMIT %s OFFSET %s"
                params.extend([records_per_page, offset])

        # 执行数据查询
        cursor.execute(query, tuple(params))
        print("Executing query:", query, tuple(params))
        results = cursor.fetchall()

        # 返回总数和数据的 JSON 响应
        return jsonify({"total": total_count, "data": results})

    except mysql.connector.Error as err:
        # 打印错误日志
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        # 关闭数据库连接
        cursor.close()
        conn.close()


@app.route('/api/getPdbFile', methods=['GET'])
def get_pdb_file():
    try:
        # 获取传入的文件路径（通过查询参数传递）
        file_path = request.args.get('filePath')

        file_path = os.path.join(pdb_folder_path[0], str(file_path))

        if not file_path:
            return jsonify({"error": "filePath parameter is required"}), 400
                        
        # 返回文件
        return send_file(file_path, as_attachment=True, mimetype='chemical/x-pdb')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/getSeqProperties', methods=['GET'])
def get_seq_properties():
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
        cursor.close()
        conn.close()

@app.route('/api/getProStruProperties', methods=['GET'])
def get_pro_stru_properties():
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
        cursor.close()
        conn.close()

@app.route('/api/getStruProperties', methods=['GET'])
def get_stru_properties():
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
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
