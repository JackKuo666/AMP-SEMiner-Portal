<template>
<el-header class="header">
  <div class="logo">
    <h2 class="portal-title">Download</h2>
  </div>
</el-header>
  <div id="download">
    <el-container>
      <el-main>
        <el-table :data="datasets" border style="width: 100%">
          <!-- 索引 -->
          <el-table-column prop="index" label="Data Index" width="130"></el-table-column>

          <!-- 数据名 -->
          <el-table-column prop="name" label="Data Name" width="450"></el-table-column>

          <!-- 描述 -->
          <el-table-column prop="description" label="Description"></el-table-column>

          <!-- 下载按钮 -->
          <el-table-column label="Download" width="150">
            <template #default="scope">
              <el-button 
                v-if="scope.row.fetchable" 
                type="primary" 
                icon="el-icon-download" 
                size="small"
                :loading="loading === scope.row.path"
                @click="download(scope.row.path)"
              >
                Download
              </el-button>
              <el-button 
                v-else
                type="primary" 
                icon="el-icon-download" 
                size="small"
              >
                <a :href="scope.row.path" download>
                  Download
                </a>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>

    </el-container>
  </div>
  <!-- 页脚 -->
    <el-footer class="footer">
      <p>Copyright © 2024 AMP-SEMiner authors All rights reserved. The portal open source code is available in <a href="https://github.com/JackKuo666/AMP-SEMiner-Portal" target="_blank" rel="noopener noreferrer" class="blue-link">this link</a>.</p>
  </el-footer>
</template>

<script>
export default {
  name: "DownloadPage",
  data() {
    return {
      // 表格数据
      datasets: [
        {
          name: "dataset.csv(902 MB)",
          index: "Online Data 1",
          description: "Training, validation, and testing datasets.",
          path: "https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/dataset.csv",
          fetchable: false, // Direct link
        },
        {
          name: "independent_test_APD.dataset.csv(2.04 MB)",
          index: "Online Data 2",
          description: "Independent testing dataset from APD.",
          path: "https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/independent_test_APD.dataset.csv",
          fetchable: true, // Use fetch for this file
        },
        {
          name: "independent_test_LAMP2.dataset.csv(1.59 MB)",
          index: "Online Data 3",
          description: "Independent testing dataset from LAMP2.",
          path: "https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/independent_test_LAMP2.dataset.csv",
          fetchable: true, // Direct link
        },
        {
          name: "all_amp_protein.animal.clst90_80.eggnog.rmdup.filter.tsv(78.8 MB)",
          index: "Online Data 4",
          description: "Sequences of representative protein clusters.",
          path: "https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/all_amp_protein.animal.clst90_80.eggnog.rmdup.filter.tsv",
          fetchable: false, // Direct link
        },
        {
          name: "all_AMPs.tsv(1.4 GB)",
          index: "Online Data 5",
          description: "All predicted AMPs.",
          path: "https://huggingface.co/datasets/jackkuo/AMP-SEMiner-dataset/resolve/main/all_AMPs.tsv",
          fetchable: false, // Direct link
        },
      ],
      // 用于控制点击按钮时的加载状态
      loading: null,
    };
  },
  methods: {
    /**
     * 触发下载
     * @param {string} filePath 文件下载路径
     */
    async download(filePath) {
      try {
        // 标记当前下载中的文件（用于按钮loading状态）
        this.loading = filePath;

        // 通过 fetch 获取文件
        const response = await fetch(filePath, { method: "GET" });
        if (!response.ok) {
          throw new Error("网络响应不正常");
        }

        // 将响应转换为 Blob
        const blob = await response.blob();

        // 创建一个本地的下载链接
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filePath.split("/").pop(); // 从路径中提取文件名
        document.body.appendChild(link);

        // 触发链接点击事件进行下载
        link.click();

        // 下载完成后清理临时节点和 URL
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("下载过程中出错:", error);
        // Element UI 的消息提示
        this.$message.error("下载失败，请稍后再试。");
      } finally {
        // 释放加载状态
        this.loading = null;
      }
    },
  },
};
</script>

<style>
.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
  h2 {
  text-align: center;
  margin: 0;
}
}

#download {
  margin: 20px;
}
.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

h2 {
  text-align: center;
  margin: 0;
}

.footer {
  margin-bottom: 0;
  text-align: center;
  padding: 20px 0;
  background-color: #409EFF;
  color: white;
}

.footer p {
  margin: 0;
  font-size: 14px;
}

.footer a {
  color: #ffeb3b;
  text-decoration: underline;
}
</style>
