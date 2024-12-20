<template>
  <div class="article-home">
    <el-container>
      <!-- 页头 -->
      <el-header class="header">
        <div class="logo">
          <el-button type="primary" size="large" class="home-button" @click="handleClick">Article title: article title article title article title article title article title</el-button>
        </div>
      </el-header>

      <!-- 主体内容 -->
      <el-main>
        <!-- 作者信息 -->
        <el-row class="authors-row">
          <el-col>
            <el-card class="authors-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h3>Authors:</h3>
              <p>{{ authors }}</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- 文章摘要 -->
        <el-row class="abstract-row">
          <el-col>
            <el-card class="article-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2>Abstract:</h2>
              <p>{{ articleSummary }}</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- 图片展示 -->
        <el-row class="picture-row" justify="center">
          <el-col :span="16">
            <el-card class="picture-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h3>Figure:</h3>
              <img :src="pictureUrl" alt="Figure Image" class="article-picture" />
            </el-card>
          </el-col>
        </el-row>


        <!-- 文章详情 -->
        <el-row class="details-row">
          <el-col>
            <el-card class="article-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2>Article details:</h2>
              <p>{{ articleDetails }}</p>
              <el-button type="primary" size="small" class="read-more-btn" @click="handleClick">Full Article</el-button>
            </el-card>
          </el-col>
        </el-row>
      </el-main>

      <!-- 页脚 -->
      <el-footer class="footer">
        <p>© 2024 AMP SEMiner authors. The resource is described in detail in link</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import picturePath from '@/assets/images/Figure_1.png';
export default {
  name: 'ArticleHome',
  data() {
    return {
      authors: 'Dr. Alice, Dr. Bob, Dr. Charlie',
      articleSummary: 'This article discusses the latest research results of xx, covering all aspects from experimental design to data analysis.',
      articleDetails: 'This article details the background, methods, and main conclusions of the experiment, and discusses relevant future research directions.',
      pictureUrl: picturePath,
    };
  },
  methods: {
    handleClick() {
      window.location.href = 'https://example.com'; // 替换为完整文章链接
    },
  },
};
</script>

<style scoped>
.article-home {
  font-family: 'Arial', sans-serif;
  background-color: #f5f7fa;
}

.header {
  background-color: #409EFF;
  justify-content: center; /* 水平方向居中 */
  text-align: center;
  padding: 20px 0;
}

.logo {
  display: inline-block;
}

.home-button {
  font-size: 24px;
  font-weight: bold;
}

.authors-row,
.picture-row,
.abstract-row,
.details-row {
  margin-top: 20px;
}

.article-card,
.authors-card,
.picture-card {
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.article-card h2,
.authors-card h3,
.picture-card h3 {
  font-size: 20px;
  color: #333;
}

.article-card p,
.authors-card p {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.article-picture {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.read-more-btn {
  margin-top: 10px;
  background-color: #409EFF;
  border-color: #409EFF;
  font-size: 14px;
}

.footer {
  text-align: center;
  padding: 20px 0;
  background-color: #409EFF;
  color: white;
}

.footer p {
  margin: 0;
  font-size: 14px;
}
</style>
