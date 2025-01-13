<template>
  <div class="help-page">
    <el-tabs v-model="activeTab" type="card">
      <!-- Data Portal -->
      <el-tab-pane label="Data Portal Documentation" name="data-portal">
        <el-collapse v-model="activeCollapse" accordion>
          <el-collapse-item title="Introduction" name="intro">
            <p>Data Portal is an AMP-SEMiner data management platform that supports data search, preview, and download functions.</p>
          </el-collapse-item>
          <el-collapse-item title="Features" name="features">
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
          </el-collapse-item>
          <el-collapse-item title="Technical Details" name="technical-details">
            <p>- Frontend built with Vue 3 and Element3.</p>
            <p>- Backend built with flask and mysql.</p>
            <p>The portal open source code is available in <a href="https://github.com/JackKuo666/AMP-SEMiner-Portal" target="_blank" rel="noopener noreferrer" style="color: blue; text-decoration: underline; font-weight: bold;">AMP-SEMiner-Portal</a>.</p>
          </el-collapse-item>
          <el-collapse-item title="FAQ" name="faq">
            <p>Pages Loading Failed: Please check your network connection or contact Menghao Guo (guomenghao@zhejianglab.org).</p>
            <p>Data Loading Failed: Try refreshing the page.</p>
          </el-collapse-item>
        </el-collapse>
      </el-tab-pane>

      <!-- AMP-SEMiner -->
      <el-tab-pane label="AMP-SEMiner Documentation" name="amp-seminer">
        <el-collapse v-model="activeCollapse" accordion>
          <el-collapse-item title="Introduction" name="intro">
            <p>AMP-SEMiner is a robust and comprehensive AI framework designed for residue-level AMP discovery. </p>
          </el-collapse-item>
          <el-collapse-item title="Usage Guide" name="usage-guide">
            <p>You can experience the full functionality in <a href="https://github.com/zjlab-BioGene/AMP-SEMiner/" target="_blank" style="color: blue; text-decoration: underline; font-weight: bold;">AMP-SEMiner</a>.</p>
            <p>Detailed Steps:</p>
            <el-divider></el-divider>
            <el-timeline>
              <el-timeline-item timestamp="Step 1">Install dependencies.</el-timeline-item>
              <el-timeline-item timestamp="Step 2">Run AMP prediction.</el-timeline-item>
              <el-timeline-item timestamp="Step 3">Run training.</el-timeline-item>
              <el-timeline-item timestamp="Step 4">Custom code for Colab Notebook.</el-timeline-item>
            </el-timeline>
          </el-collapse-item>
          <el-collapse-item title="Technical Details" name="technical-details">
            <p>- Core Algorithm: Deep learning model based on sequence features.</p>
            <p>- Data Processing: Uses standardized pipeline to process raw sequences.</p>
          </el-collapse-item>
          <el-collapse-item title="FAQ" name="faq">
            <p>Notebook Not Running: Ensure Python version is 3.10 and PyTorch 2.1.2.</p>
            <p>Dependency Installation Failed: Check pip version.</p>
          </el-collapse-item>
        </el-collapse>
      </el-tab-pane>
    </el-tabs>
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
      activeTab: 'data-portal',
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
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.el-tabs {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.el-collapse {
  margin-top: 20px;
}

.el-collapse-item {
  text-align: left;
}

.el-timeline {
  margin-top: 10px;
}

/* Feature section styling */
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

/* Image styling */
.feature-image {
  margin-top: 20px;
  width: 80%; /* Adjust width as necessary */
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
</style>