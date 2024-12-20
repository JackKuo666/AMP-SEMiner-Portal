<template>
  <el-container direction="vertical">
    <el-header>
      <h1>Gene Information Page</h1>
    </el-header>
    <el-main>
      <el-card class="sequence-card">
        <template #header>
          <div class="card-header">
            <span>Sequence</span>
          </div>
        </template>
        <div class="sequence-content">
          <span v-for="(char, index) in geneInfo.sequence" :key="index"
                :class="{ 'highlight': index >= geneInfo.pos[0]  && index <= geneInfo.pos[1]  }">
            {{ char }}
          </span>
        </div>
      </el-card>

      <el-row :gutter="20" style="margin-top: 20px; display: flex; align-items: stretch;">
        <el-col :span="12" style="display: flex; flex-direction: column;">
          <el-card style="flex-grow: 1;">
            <template #header>
              <div class="card-header">
                <span>Basic Information</span>
              </div>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="Protein ID">
                <el-tooltip :content="geneInfo.proteinId" placement="top">
                  <span>{{ geneInfo.proteinId.length > 20 ? geneInfo.proteinId.slice(0, 20) + '...' : geneInfo.proteinId }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="Organism">
                <el-tooltip :content="geneInfo.organism" placement="top">
                  <span>{{ geneInfo.organism.length > 20 ? geneInfo.organism.slice(0, 20) + '...' : geneInfo.organism }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="Sequence Length">{{ geneInfo.sequenceLength }}</el-descriptions-item>
              <el-descriptions-item label="Source">
                <el-tooltip :content="geneInfo.source" placement="top">
                  <span>{{ geneInfo.source.length > 20 ? geneInfo.source.slice(0, 20) + '...' : geneInfo.source }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="ProID">
                <el-tooltip :content="geneInfo.proId" placement="top">
                  <span>{{ geneInfo.proId.length > 20 ? geneInfo.proId.slice(0, 20) + '...' : geneInfo.proId }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="AMP">
                <el-tooltip :content="geneInfo.amp" placement="top">
                  <el-link type="primary" @click="handleAmpClick">
                    {{ geneInfo.amp.length > 20 ? geneInfo.amp.slice(0, 20) + '...' : geneInfo.amp }}
                  </el-link>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="AMPlen">{{ geneInfo.ampLen }}</el-descriptions-item>
              <el-descriptions-item label="Position">{{ geneInfo.position }}</el-descriptions-item>
              <el-descriptions-item label="Pro_clst80">{{ geneInfo.proClst80 }}</el-descriptions-item>
              <el-descriptions-item label="AMP_clst">{{ geneInfo.ampClst }}</el-descriptions-item>
              <el-descriptions-item label="seed_ortholog">{{ geneInfo.seedOrtholog }}</el-descriptions-item>
              <el-descriptions-item label="GOs">
                <el-tooltip :content="geneInfo.gos" placement="top" effect="dark">
                  <span>{{ geneInfo.gos.length > 20 ? geneInfo.gos.slice(0, 20) + '...' : geneInfo.gos }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="KEGG_ko">
                <el-tooltip :content="geneInfo.keggKo" placement="top" effect="dark">
                  <span>{{ geneInfo.keggKo && geneInfo.keggKo.length > 20 ? geneInfo.keggKo.slice(0, 20) + '...' : geneInfo.keggKo }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="KEGG_Pathway">
                <el-tooltip :content="geneInfo.keggPathway" placement="top" effect="dark">
                  <span>{{ geneInfo.keggPathway && geneInfo.keggPathway.length > 20 ? geneInfo.keggPathway.slice(0, 20) + '...' : geneInfo.keggPathway }}</span>
                </el-tooltip>
              </el-descriptions-item>
              <el-descriptions-item label="CID">{{ geneInfo.cid }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
       <el-col :span="12" style="display: flex; flex-direction: column;">
          <el-card style="flex-grow: 1;">
            <template #header>
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <!-- Title on the left -->
                <span>3D Structure (AlphaFold2)</span>
                <!-- Buttons on the right -->
                <div>
                  <el-button type="primary" @click="downloadPdbPro" size="mini">Download Protein PDB</el-button>
                  <el-button type="primary" @click="downloadPdbAmp" size="mini">Download AMP PDB</el-button>
                </div>
              </div>
            </template>
            <div ref="nglViewer" style="width: 100%; height: 400px;"></div>
          </el-card>
        </el-col>
      </el-row>
      <el-row v-if="ampProperties.length > 0" :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>AMP Sequence Properties</span>
              </div>
            </template>
            <el-descriptions :column="2" style="width: 100%" border>
              <el-descriptions-item label="AMPlen">{{ ampProperties[0].AMPlen }}</el-descriptions-item>
              <el-descriptions-item label="Net Charge">{{ ampProperties[0].netCharge }}</el-descriptions-item>
              <el-descriptions-item label="Molecular Weight">{{ ampProperties[0].molWeight }}</el-descriptions-item>
              <el-descriptions-item label="Avg Hydrophobicity">{{ ampProperties[0].avgHydro }}</el-descriptions-item>
              <el-descriptions-item label="Isoelectric Point">{{ ampProperties[0].isoelectricPoint }}</el-descriptions-item>
              <el-descriptions-item label="Boman Index">{{ ampProperties[0].BomanIndex }}</el-descriptions-item>
              <el-descriptions-item label="Solubility Rules Failed">{{ ampProperties[0].Solubility_rules_failed }}</el-descriptions-item>
              <el-descriptions-item label="Synthesis Rules Failed">{{ ampProperties[0].Synthesis_rules_failed }}</el-descriptions-item>
              <el-descriptions-item label="Crippen LogP">{{ ampProperties[0].CrippenLogP }}</el-descriptions-item>
              <el-descriptions-item label="Max Hydrophobic Moment">{{ ampProperties[0].maxHydrophobicMoment }}</el-descriptions-item>
              <el-descriptions-item label="Mean Hydrophobic Moment">{{ ampProperties[0].meanHydrophobicMoment }}</el-descriptions-item>
              <el-descriptions-item label="Hydrophobic Moment">{{ ampProperties[0].HydrophobicMoment }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
      </el-row>
      <el-card class="structure-card" v-if="proStruProperties.length > 0">
        <template #header>
          <div class="card-header">
            <span>Protein Structure Properties</span>
          </div>
        </template>
        <el-descriptions :column="2" style="width: 100%" border>
          <el-descriptions-item label="ProteinID">{{ proStruProperties[0].ProteinID }}</el-descriptions-item>
          <el-descriptions-item label="Rg">{{ proStruProperties[0].Rg }}</el-descriptions-item>
          <el-descriptions-item label="RgNorm">{{ proStruProperties[0].RgNorm }}</el-descriptions-item>
          <el-descriptions-item label="Area">{{ proStruProperties[0].Area }}</el-descriptions-item>
          <el-descriptions-item label="AreaPerResi">{{ proStruProperties[0].AreaPerResi }}</el-descriptions-item>
          <el-descriptions-item label="MinSemiAxes">{{ proStruProperties[0].MinSemiAxes }}</el-descriptions-item>
          <el-descriptions-item label="Loop">{{ proStruProperties[0].Loop }}</el-descriptions-item>
          <el-descriptions-item label="Coil">{{ proStruProperties[0].Coil }}</el-descriptions-item>
          <el-descriptions-item label="Assort">{{ proStruProperties[0].Assort }}</el-descriptions-item>
          <el-descriptions-item label="Q">{{ proStruProperties[0].Q }}</el-descriptions-item>
          <el-descriptions-item label="Dim">{{ proStruProperties[0].Dim }}</el-descriptions-item>
          <el-descriptions-item label="CVHP">{{ proStruProperties[0].CVHP }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      <el-card class="structure-card" v-if="struProperties.length > 0">
        <template #header>
          <div class="card-header">
            <span>AMP Structure Properties</span>
          </div>
        </template>
        <el-descriptions :column="2" style="width: 100%" border>
          <el-descriptions-item label="Rg">{{ struProperties[0].Rg }}</el-descriptions-item>
          <el-descriptions-item label="RgNorm">{{ struProperties[0].RgNorm }}</el-descriptions-item>
          <el-descriptions-item label="Area">{{ struProperties[0].Area }}</el-descriptions-item>
          <el-descriptions-item label="AreaPerResi">{{ struProperties[0].AreaPerResi }}</el-descriptions-item>
          <el-descriptions-item label="MinSemiAxes">{{ struProperties[0].MinSemiAxes }}</el-descriptions-item>
          <el-descriptions-item label="Loop">{{ struProperties[0].Loop }}</el-descriptions-item>
          <el-descriptions-item label="Coil">{{ struProperties[0].Coil }}</el-descriptions-item>
          <el-descriptions-item label="Assort">{{ struProperties[0].Assort }}</el-descriptions-item>
          <el-descriptions-item label="Q">{{ struProperties[0].Q }}</el-descriptions-item>
          <el-descriptions-item label="Dim">{{ struProperties[0].Dim }}</el-descriptions-item>
          <el-descriptions-item label="CVHP">{{ struProperties[0].CVHP }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      <el-card class="amp-card" v-if="tableData.length > 0">
        <template #header>
          <div class="card-header">
            <span>SAME AMPs</span>
            <!-- 下载按钮 -->
            <el-button
              size="small"
              type="primary"
              @click="downloadTableData"
              style="float: right; margin-right: 10px;">
              Download
            </el-button>
          </div>
        </template>

        <!-- 表格部分 -->
        <el-table
          :data="tableData.slice(0, 15)"
          border
          style="margin-top: 10px;">
          <!-- 动态渲染列 -->
          <template v-for="item in tableLabel" :key="item.prop">
            <el-table-column
              :prop="item.prop"
              :label="item.label"
              :width="item.width ? item.width : 125"
              sortable
            />
          </template>
        </el-table>
        <!-- 显示数据被截断的提示 -->
        <div v-if="tableData.length > 15" style="margin-top: 10px; text-align: center; color: #999;">
          Showing first 15 rows. Download for full data.
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import {ref, onMounted, getCurrentInstance, reactive} from 'vue'
import * as NGL from 'ngl'
import { ElMessage } from 'element-plus'; // 引入ElMessage

import { useRoute } from 'vue-router';
const {proxy} = getCurrentInstance()

const oneGeneData = ref(null);
const nglViewer = ref(null)
const geneInfo = ref({
  proteinId: 'AXC42625.1',
  organism: 'Homo sapiens',
  sequenceLength: 100,
  sequence: 'MILIFKTAERTFLMTHNNYIYILVMALVSYAIRVLPLTLIRKPIKNQFIQSFLYYVPYVTLAVMTFPAIVEATQSPLAGAVALVVGIAAAWFGASLFQVSVACCAVVFVIELFI',
  pos: [34, 44],
  source: 'data_Hadza',
  proId: 'ERZ6619726.19_11',
  amp: 'LPLTLIRKPIK',
  ampLen: 11,
  position: '34,44',
  proClst80: 90,
  ampClst: 0,
  seedOrtholog: '-',
  gos: '-',
  keggKo: '-',
  keggPathway: '-',
  cid: 'C224992',
  ampPdb: '',
  proPdb: ''
})


// 获取PDB文件的URL
const fetchPdbUrlAmp = async () => {
  try {
    const a = oneGeneData.value.AMP_clst +
        "|" + oneGeneData.value.Pro_clst80 +
        "|" + oneGeneData.value.Pro_clst +
        "|" + oneGeneData.value.CID +
        ":" + (geneInfo.value.pos[0]+1) +
        "-" + (geneInfo.value.pos[1]+1)
    // 使用 proxy.$api.getPdbFile 获取 PDB 文件
    const response = await proxy.$api.getPdbFile({filePath:"AMP_fragment_pdbs/"+a+".pdb"});
    return response
  } catch (error) {
    console.error("Error fetching PDB file URL:", error);
    return null
  }
};

const proPdbResponse = ref(null)
// 获取PDB文件的URL
const fetchPdbUrlPro = async () => {
  try {
    // 使用 proxy.$api.getPdbFile 获取 PDB 文件
    const response = await proxy.$api.getPdbFile({filePath:"Pro_clst80_pdbs/"+oneGeneData.value.CID+".pdb"});
    proPdbResponse.value = response
    return response
  } catch (error) {
    console.error("Error fetching PDB file URL:", error);
    return null
  }
};
onMounted(async () => {
  const oneGeneDataGet = localStorage.getItem('oneGeneData'); // 从 localStorage 中获取数据
  oneGeneData.value = oneGeneDataGet ? JSON.parse(oneGeneDataGet) : {}; // 解析 JSON，如果为空则设置为空对象
  console.log("oneGeneData",oneGeneData.value)
  // 将 oneGeneData 的数据更新给 geneInfo
  if (oneGeneData.value) {
    geneInfo.value = {
      proteinId: oneGeneData.value.ID || '-',
      organism: oneGeneData.value.organism || '-',
      sequenceLength: oneGeneData.value.Sequence ? oneGeneData.value.Sequence.length : 0,
      sequence: oneGeneData.value.Sequence || '',
      pos: oneGeneData.value.Position ? oneGeneData.value.Position.split(',').map(Number) : [0, 0],
      source: oneGeneData.value.Source || '',
      proId: oneGeneData.value.ProID || '',
      amp: oneGeneData.value.AMP || '',
      ampLen: oneGeneData.value.AMPlen || 0,
      position: oneGeneData.value.Position || '',
      proClst80: oneGeneData.value.Pro_clst80 || 0,
      ampClst: oneGeneData.value.AMP_clst || 0,
      seedOrtholog: oneGeneData.value.seed_ortholog || '-',
      gos: oneGeneData.value.GOs || '-',
      keggKo: oneGeneData.value.KEGG_ko || '-',
      keggPathway: oneGeneData.value.KEGG_Pathway || '-',
      cid: oneGeneData.value.CID || '',
      ampPdb: oneGeneData.value.AMPpdb || '',
      proPdb: oneGeneData.value.PDB || '',
    };
  }
  fetchSeqProperties()
  fetchProStruProperties()
  fetchStruProperties()
  console.log("geneInfo.value.proPdb", geneInfo.value.proPdb)
  console.log("geneInfo.value.ampPdb", geneInfo.value.ampPdb)
  if (!geneInfo.value.proPdb) {
        // 如果没有值，显示绿色提示
        ElMessage.success('PDB value is missing!');
      }
  // 请求PDB文件的URL并加载到NGL Stage
  const pdbData = await fetchPdbUrlPro();
  if (!pdbData) return; // 如果未能获取数据则退出
  // console.log("pdbData:", pdbData)

  const stage = new NGL.Stage(nglViewer.value, { backgroundColor: "white" })

  stage.loadFile(new Blob([pdbData], { type: 'text/plain' }), { ext: 'pdb' }).then((component) => {
    component.addRepresentation('cartoon', {
      color: 'blue',
    })
    if (geneInfo.value.pos[0] && geneInfo.value.pos[1]) {
      const selection = new NGL.Selection(`${geneInfo.value.pos[0]}-${geneInfo.value.pos[1]}`);
      component.addRepresentation('cartoon', { sele: selection.string, color: 'red' });
    }
    component.autoView()
  })
})

const downloadPdbAmp = async () => {
  const pdbData = await fetchPdbUrlAmp();
  if (!pdbData) return; // 如果未能获取数据则退出

  // 创建 Blob 对象并下载文件
  const blob = new Blob([pdbData], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${geneInfo.value.proteinId}_amp.pdb`;
  link.click();

  // 释放内存
  URL.revokeObjectURL(link.href);
};

const downloadPdbPro = async () => {
  const pdbData = proPdbResponse.value;
  if (!pdbData) return; // 如果未能获取数据则退出

  // 创建 Blob 对象并下载文件
  const blob = new Blob([pdbData], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${geneInfo.value.proteinId}_protein.pdb`;
  link.click();

  // 释放内存
  URL.revokeObjectURL(link.href);
};


//其中total是数据总条数，page是当前的页数，设置name根据name进行条件搜索
const config = reactive({
  tables: 'all_amp_protein_animal',
  amp_same: 1,
  total_page: 100,
  records_per_page: 10,
  page: 1,
  source: '',
  amp: '',
  proClst80: NaN,
  amplenmin: 1,
  amplenmax: 500,
  sortProp: '',
  sortOrder: ''
})

const tableLabel = reactive([
  {
    prop: "Source",
    label: "Source",
  },
  {
    prop: "ProID",
    label: "ProID",
  },
  {
    prop: "AMP",
    label: "AMP",
  },
  {
    prop: "AMPlen",
    label: "AMPlen",
  },
  {
    prop: "Position",
    label: "Position",
  },
  {
    prop: "Sequence",
    label: "Sequence", // 外链：内部
  },
  {
    prop: "Pro_clst80",
    label: "Pro_clst80",
  },
  {
    prop: "AMP_clst",
    label: "AMP_clst",
  },
  {
    prop: "seed_ortholog",  // 链接：外部
    label: "seed_ortholog",
  },
  {
    prop: "GOs",   // 链接：外部
    label: "GOs",
  },
  {
    prop: "KEGG_ko",
    label: "KEGG_ko",
  },
  {
    prop: "KEGG_Pathway",
    label: "KEGG_Pathway",
  },
  {
    prop: "CID",
    label: "CID",
  },
]);



// 获取 AMP 相关的属性
const handleAmpClick = async () => {
  try {
    // 在这里添加实际的搜索逻辑
    config.amp = oneGeneData.value.AMP
    getAllAmpsData(); // 调用数据获取函数

  } catch (error) {
    console.error("Error fetching AMP properties:", error);
    ampProperties.value = [];  // 出现错误时清空数据
  }
}
const tableData = ref([])

const getAllAmpsData = async () => {
  try {
    // 调用 API 获取数据
    const response = await proxy.$api.getAllAmpsData(config);
    console.log("response", response);

    // 处理 API 返回的数据
    if (response && response.data) {
      // 更新表格数据
      tableData.value = response.data.map(item => ({
        ...item,
      }));

      // 更新总记录数
      config.total_page = Math.floor(response.total / config.records_per_page);
      console.log(`Total records: ${config.total_page}`);
    } else {
      console.log("No data returned from the API.");
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};

// 下载表格数据
const downloadTableData = () => {
  const csvContent = [
    tableLabel.map(label => label.label).join(","), // 表头
    ...tableData.value.map(row =>
      tableLabel.map(item => row[item.prop] ?? "").join(",")
    )
  ].join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", oneGeneData.value.AMP+"_table_data.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const ampProperties = ref([]);  // 用来存储返回的 AMP 数据

// 获取 AMP 相关的属性
const fetchSeqProperties = async () => {
  try {
    // 发送请求到后端，使用 proxy.$api.getSeqProperties
    const response = await proxy.$api.getSeqProperties({
      amp: geneInfo.value.amp  // 将 AMP 值作为参数传递
    });

    // 假设返回的数据结构为 { data: [...] }
    if (response.data && response.data.length > 0) {
      ampProperties.value = response.data;  // 保存返回的数据
    } else {
      ampProperties.value = [];  // 如果没有数据，则清空
    }
  } catch (error) {
    console.error("Error fetching AMP properties:", error);
    ampProperties.value = [];  // 出现错误时清空数据
  }
}
const proStruProperties = ref([])

const fetchProStruProperties = async () => {
  try {
    console.log(geneInfo.value.cid)
    const response = await proxy.$api.getProStruProperties({
      protein_id: geneInfo.value.cid  // 你可以动态获取这个值
    })
    console.log("response.data", response.data)
    // 假设返回的数据结构为 { data: [...] }
    if (response.data && response.data.length > 0) {
      proStruProperties.value = response.data;  // 保存返回的数据
    } else {
      proStruProperties.value = {};  // 如果没有数据，则清空
    }
    console.log("proStruProperties", proStruProperties)
  } catch (error) {
    console.error("Error fetching protein structure properties:", error)
  }
}

const struProperties = ref([]);  // 存储返回的结构数据

// 假设使用 proxy.$api.getStruProperties 请求接口获取数据
const fetchStruProperties = async () => {
  try {

    const a = oneGeneData.value.AMP_clst +
        "|" + oneGeneData.value.Pro_clst80 +
        "|" + oneGeneData.value.Pro_clst +
        "|" + oneGeneData.value.CID +
        ":" + (geneInfo.value.pos[0]+1) +
        "-" + (geneInfo.value.pos[1]+1)

    // console.log("a", a)
    const response = await proxy.$api.getStruProperties({
      protein_id: a  // 你可以动态获取这个值
    });  // 调用后端接口获取数据
    if (response.data && response.data.length > 0) {
      struProperties.value = response.data;  // 保存返回的数据
    } else {
      struProperties.value = [];  // 如果没有数据，则清空
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    struProperties.value = [];  // 如果请求失败，清空数据
  }
}
</script>

<style scoped>
.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sequence-card {
  margin-bottom: 20px;
}

.sequence-content {
  font-family: monospace;
  font-size: 16px;
  line-height: 1.5;
  word-wrap: break-word;
}

.sequence-content span {
  display: inline-block;
  margin-right: 1px;
}

.highlight {
  color: red;
  font-weight: bold;
}
</style>