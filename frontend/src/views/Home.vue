<template>
  <div class="article-home">
    <el-container>
      <!-- 页头 -->
      <el-header class="header">
        <div class="logo">
          <h2 class="portal-title">MAG-AMPome</h2>
        </div>
      </el-header>

      <!-- 主体内容 -->
      <el-main>
        <!-- 数据门户名称与描述 -->
        <el-row class="portal-row">
          <el-col>
            <el-card class="portal-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Description</h2>
              <p class="section-text">A Data Portal for Antimicrobial Peptides from Metagenome-Assembled Genomes.</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- Contributors Section -->
        <el-row class="contributors-row">
          <el-col>
            <el-card class="contributors-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Contributors</h2>
              <p class="section-text">
                <strong>Wenhui Li</strong> 
                (<a href="mailto:liwh@tongji.edu.cn" class="blue-link">liwh@tongji.edu.cn</a>, 
                <a href="mailto:jemimalwh@gmail.com" class="blue-link">jemimalwh@gmail.com</a>), 
                <strong>Baicheng Huang</strong> 
                (<a href="mailto:huangbc@zhejianglab.org" class="blue-link">huangbc@zhejianglab.org</a>), 
                <strong>Menghao Guo</strong> 
                (<a href="mailto:guomenghao@zhejianglab.org" class="blue-link">guomenghao@zhejianglab.org</a>)
              </p>
            </el-card>
          </el-col>
        </el-row>

        <!-- Correspondence Section -->
        <el-row class="correspondence-row">
          <el-col>
            <el-card class="correspondence-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Correspondence</h2>
              <p class="section-text">
                <strong>Jinfang Zheng</strong> 
                (<a href="mailto:zhengjinfang1220@gmail.com" class="blue-link">zhengjinfang1220@gmail.com</a>)
              </p>
            </el-card>
          </el-col>
        </el-row>

        <!-- Abstract Section -->
        <el-row class="abstract-row">
          <el-col>
            <el-card class="abstract-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Abstract</h2>
              <p class="section-text">Antimicrobial resistance is an escalating threat to public health, underscoring the urgent need for innovative therapeutic solutions. Antimicrobial peptides (AMPs), short protein sequences with diverse mechanisms of action, represent a promising alternative due to their broad-spectrum activity against pathogens. Advances in protein language models (PLMs) have transformed protein structure prediction and functional annotation, opening new avenues for AMP discovery and therapeutic development.</p>
              <p class="section-text">We introduce AMP-SEMiner (Antimicrobial Peptide Structural Evolution Miner, <a href="https://github.com/zjlab-BioGene/AMP-SEMiner" target="_blank" rel="noopener noreferrer" class="blue-link">AMP-SEMiner</a>), an AI-powered framework that identifies AMPs from metagenome-assembled genomes (MAGs). Using AMP-SEMiner, we have uncovered 1,670,600 AMP candidates, including those encoded by small open reading frames (smORFs) and encrypted peptides (EPs), sourced from diverse habitats, significantly expanding the known AMP discovery landscape.</p>
              <p class="section-text">The MAG-AMPome portal offers access to this vast repository of AMPs identified from metagenome-assembled genomes, with a focus on diverse human-gut habitats. The portal provides both AMP sequences and their predicted structures, serving as a valuable resource for researchers exploring novel antimicrobial strategies.</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- 图表展示 -->
        <el-row class="figures-tables-row" justify="center">
          <el-col :span="16">
            <el-card class="figures-tables-card" shadow="hover" :body-style="{ padding: '20px' }">
              <!-- Collapsible Figures and Tables -->
              <el-collapse v-model="activeNames" accordion>
                <el-collapse-item v-for="(item, index) in figures" :key="index" :title="item.title" :name="index">
                  <div class="figure-content">
                    <img :src="item.src" alt="Figure" class="figure-image" @error="event => onImageError(event, index)" />
                    <p class="figure-description">{{ item.description }}</p>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </el-card>
          </el-col>
        </el-row>

        <!-- 工具与链接 -->
        <el-row class="tool-row">
          <el-col>
            <el-card class="tool-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h2 class="section-title">Tool</h2>
              <p class="section-text">AMP-SEMiner: Explore the tool on <a href="https://github.com/zjlab-BioGene/AMP-SEMiner" target="_blank" rel="noopener noreferrer" class="blue-link">GitHub</a></p>
            </el-card>
          </el-col>
        </el-row>

        <!-- 引用信息 -->
        <el-row class="citation-row">
          <el-col>
            <el-card class="citation-card" shadow="hover" :body-style="{ padding: '20px' }">
              <h3 class="section-title">Citation</h3>
              <p class="section-text">Please cite this tool as: <i>Unveiling the Evolution of Antimicrobial Peptides in Gut Microbes via Foundation Model-Powered Framework, DOI: TBD</i></p>
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
import picturePath1 from '@/assets/images/Figure_1.png';
import picturePath2 from '@/assets/images/Stat.1.png';
import picturePath3 from '@/assets/images/Stat.2.png';
import picturePath4 from '@/assets/images/Stat.3.png';
import picturePath5 from '@/assets/images/Stat.4.png';
import picturePath6 from '@/assets/images/Stat.5.png';

export default {
  name: 'ArticleHome',
  data() {
    return {
      figures: [
        { title: 'Fig. 1', description: 'Fig. 1. Schematic overview of the AMP-SEMiner framework.', src: picturePath1 },
        { title: 'Fig. 2', description: 'Fig. 2. Sankey diagram depicting the distribution of approximately 1 million predicted AMPs across various habitats.', src: picturePath2 },
        { title: 'Fig. 3', description: 'Fig. 3. Chord diagram illustrating the interrelationships between predicted AMPs from different habitats.', src: picturePath3 },
        { title: 'Fig. 4', description: 'Fig. 4. Lineage frequency of AMP-containing genes, categorized at the phylum level. AHG refers to ancient human gut microbiomes, while MHG represents modern human gut microbiomes from the MGnify database.', src: picturePath4 },
        { title: 'Fig. 5', description: 'Fig. 5. Physicochemical properties of AMP sequences: net charge, isoelectric point, hydrophobic moment, boman index, average hydropathy, Crippen LogP.', src: picturePath5 },
        { title: 'Fig. 6', description: 'Fig. 6. Violin diagrams of structural properties for AMP-containing proteins from the APD3 and LAMP2 databases (shown in orange and green, respectively) compared to those identified in this study (shown in pink).', src: picturePath6 }
      ], 
      activeNames: [0] // 默认展开第一个折叠项
    };
  },
  methods: {
    onImageError(event, index) {
      console.warn(`Image at index ${index} failed to load.`);
      event.target.src = require('@/assets/images/404.png'); // 设置默认图片路径
    }
  }
};
</script>

<style scoped>
.article-home {
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
  .portal-title {
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.portal-subtitle {
  font-size: 16px;
  font-weight: 600; 
  color: #d1e7ff;
  display: block;
  margin-top: 10px;
}
}


.logo {
  display: inline-block;
}



.portal-row,
.contributors-row,
.correspondence-row,
.abstract-row,
.figures-tables-row,
.tool-row,
.citation-row {
  margin-top: 20px;
}

.portal-card,
.contributors-card,
.correspondence-card,
.abstract-card,
.figures-tables-card,
.tool-card,
.citation-card {
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.portal-card h2 {
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}

.section-text {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
  text-align: left; /* 明确设置文本对齐方式 */
}

.contributors-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.correspondence-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.abstract-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.figures-tables-card h3,
.tool-card h2{
  font-size: 20px;
  color: #333;
  text-align: left; /* 明确设置文本对齐方式 */
}
.citation-card h3 {
  font-size: 20px;
  color: #333;
}

.portal-card p,
.contributors-card p,
.correspondence-card p,
.abstract-card p,
.figures-tables-card p,
.tool-card p,
.citation-card p {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.figure-image {
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

.el-collapse-item__header {
  text-align: center; /* 标题居中 */
}

.el-collapse-item__header.is-active {
  text-align: center; /* 确保激活状态下的标题也居中 */
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
</style>