<template>
  <div class="help-page">
    <el-container>
      <!-- 页头 -->
      <el-header class="header">
        <div class="logo">
          <h2 class="portal-title">Help</h2>
        </div>
      </el-header>

      <!-- 主体内容 -->
      <el-main>
        <!-- 数据门户名称与描述 -->
        <el-row class="portal-row">
          <el-col>
            <el-card class="portal-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Introduction</h2>
              <p class="section-text">Data Portal is an AMP-SEMiner data management platform that supports data search, preview, and download functions.</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- Features Section -->
        <el-row class="features-row">
          <el-col>
            <el-card class="features-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Features</h2>
              <div class="features-container">
                <div class="feature-item">
                  <div class="feature-title">Data Search</div>
                  <p>Users can quickly find target data using keywords.</p>
                  <img :src="pictureUrl1" alt="Data Search" class="feature-image" />
                </div>
                <div class="feature-item">
                  <div class="feature-title">Data Preview</div>
                  <p>Supports viewing detailed information of Gene.</p>
                  <img :src="pictureUrl2" alt="Data Search" class="feature-image" />
                  <img :src="pictureUrl3" alt="Data Search" class="feature-image" />
                  <img :src="pictureUrl4" alt="Data Search" class="feature-image" />
                </div>
                <div class="feature-item">
                  <div class="feature-title">Data Download</div>
                  <p>Provides online data download options.</p>
                  <img :src="pictureUrl5" alt="Data Search" class="feature-image" />
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- Technical Details Section -->
        <el-row class="technical-details-row">
          <el-col>
            <el-card class="technical-details-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Technical Details</h2>
              <p>- Frontend built with Vue 3 and Element3.</p>
              <p>- Backend built with flask and mysql.</p>
              <p>The portal open source code is available in <a href="https://github.com/JackKuo666/AMP-SEMiner-Portal" target="_blank" rel="noopener noreferrer" class="blue-link">AMP-SEMiner-Portal</a>.</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- FAQ Section -->
        <el-row class="faq-row">
          <el-col>
            <el-card class="faq-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">FAQ</h2>
              <p>Pages Loading Failed: Please check your network connection or contact <strong>Menghao Guo</strong> (<a href="mailto:guomenghao@zhejianglab.org" class="blue-link">guomenghao@zhejianglab.org</a>).</p>
              <p>Data Loading Failed: Try refreshing the page.</p>
            </el-card>
          </el-col>
        </el-row>
      </el-main>

      <!-- 页脚 -->
      <el-footer class="footer">
        <p>Copyright © 2024 AMP-SEMiner authors All rights reserved. The portal open source code is available in <a href="https://github.com/JackKuo666/AMP-SEMiner-Portal" target="_blank" rel="noopener noreferrer" class="blue-link">this link</a>.</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import picturePath1 from '@/assets/images/data_1.png';
import picturePath2 from '@/assets/images/data_2.png';
import picturePath3 from '@/assets/images/data_3.png';
import picturePath4 from '@/assets/images/data_4.png';
import picturePath5 from '@/assets/images/data_5.png';

export default {
  name: 'Help',
  data() {
    return {
      pictureUrl1: picturePath1,
      pictureUrl2: picturePath2,
      pictureUrl3: picturePath3,
      pictureUrl4: picturePath4,
      pictureUrl5: picturePath5,
    };
  },
};
</script>

<style scoped>
.help-page {
  font-family: 'Arial', sans-serif;
  background-color: #f5f7fa;
}

.header {
  background-color: #409EFF;
  justify-content: center;
  text-align: center;
  padding: 20px 0;
  display: flex;
  align-items: center;
}

.logo {
  display: inline-block;
}


.portal-subtitle {
  font-size: 16px;
  font-weight: 600; 
  color: #d1e7ff;
  display: block;
  margin-top: 10px;
}

.portal-row,
.features-row,
.technical-details-row,
.faq-row {
  margin-top: 20px;
}

.portal-card,
.features-card,
.technical-details-card,
.faq-card {
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.portal-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.features-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.technical-details-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.faq-card h2 {
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}

.portal-card p,
.features-card p,
.technical-details-card p,
.faq-card p {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.feature-image {
  width: 100%; /* 确保图片宽度不超过容器宽度 */
  height: auto; /* 自动调整高度以保持宽高比 */
  border-radius: 8px;
  display: block; /* 确保图片可见 */
  object-fit: contain; /* 确保图片内容完整显示 */
}

.figure-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%; /* 确保容器宽度为100% */
}
.figure-description {
  margin-top: 10px;
  text-align: center; /* 描述居中 */
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

.footer a {
  color: #ffeb3b;
  text-decoration: underline;
}

/* 新增的样式类 */
.center-text {
  text-align: center;
}

.blue-link {
  color: blue; /* 设置链接颜色为蓝色 */
  text-decoration: underline; /* 保持下划线 */
}

.features-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
  align-items: center;
}

.feature-item {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 80%;
  transition: all 0.3s ease;
  text-align: center; /* Center the text inside the feature item */
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  text-align: center; /* Ensure the title is centered */
}

.feature-item p {
  color: #666;
  font-size: 14px;
}
</style>