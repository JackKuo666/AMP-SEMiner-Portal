<template>
  <!-- 页头 -->
<el-header class="header">
  <div class="logo">
    <h2 class="portal-title">Browse</h2>
  </div>
</el-header>
<!--  上部新增和搜索-->
  <div class="user-header">
    <el-form :inline="true" ref="formRef" :model="searchForm" label-width="120px" class="demo-form-inline">
      <el-form-item label="Source">
        <el-select
          v-model="searchForm.source"
          placeholder="Select or enter source"
          filterable
          allow-create
          default-first-option
          style="min-width: 200px;max-width: 300px;"
        >
          <el-option
            v-for="source in sources"
            :key="source.value"
            :label="source.label"
            :value="source.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="AMP Length Min">
        <el-input-number v-model="searchForm.amplenmin"
                         placeholder="Enter AMP Length Min" :min="1" :max="500" />
      </el-form-item>
      <el-form-item label="AMP Length Max">
        <el-input-number v-model="searchForm.amplenmax"
                         placeholder="Enter AMP Length Max"  :min="1" :max="500" />
      </el-form-item>
      <el-form-item label="AMP">
        <el-autocomplete
          v-model="searchForm.amp"
          :fetch-suggestions="querySearch"
          placeholder="Enter AMP"
          style="width: 500px;"
          @select="handleSelect"
          popper-class="autocomplete-popper"
          fit-input-width 
        >
          <!-- 自定义下拉菜单内容 -->
          <template #default="{ item }">
            <div class="suggestion-item">{{ item }}</div>
          </template>
      </el-autocomplete>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :disabled="!isValidForm" @click="onSearch">Search</el-button>
        <el-button @click="resetForm">Reset</el-button>
      </el-form-item>
    </el-form>
  </div>
<!--  下部表格-->
  <div class="table" v-loading="loading">
    <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
      <!-- 遍历表格列 -->
      <template v-for="item in tableLabel">
        <!-- 自定义 ProID 列，仅显示前10个字符，鼠标悬停时显示完整内容 -->
        <el-table-column
            v-if="item.prop === 'GOs' || item.prop === 'KEGG_ko' || item.prop === 'KEGG_Pathway'"
            :key="item.prop"
            :width="item.width ? item.width : 150"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-tooltip
                v-if="row[item.prop] && row[item.prop] !== '-'"
                class="item"
                effect="dark"
                placement="top"
            >
              <!-- 悬浮窗内容 -->
              <template #content>
                <div>
                  <el-link
                      v-for="go in row[item.prop]?.split(',')"
                      :key="go"
                      :href="item.prop === 'GOs' ? `https://www.ebi.ac.uk/QuickGO/GTerm?id=${go}`
                             : `https://www.genome.jp/dbget-bin/www_bget?${go.trim()}`"
                      target="_blank"
                      type="primary"
                      style="margin-right: 5px; display: inline-block;"
                  >
                    {{ go }}
                  </el-link>
                </div>
              </template>
              <!-- 表格中显示简略内容 -->
              <span style="color: #409EFF;">
                {{ row[item.prop] && row[item.prop].length > 10 ? row[item.prop].slice(0, 10) + "..." : row[item.prop] }}
              </span>
            </el-tooltip>
            <span v-else>
              {{ row[item.prop] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
            v-else-if="item.prop === 'ProID' || item.prop === 'AMP' || item.prop === 'seed_ortholog' "
            :key="item.prop"
            :width="item.width ? item.width : 150"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-tooltip
                class="item"
                effect="dark"
                :content="row[item.prop]"
                placement="top"
                :style="{ 'max-width': '200px', 'white-space': 'normal', 'word-wrap': 'break-word' }"
            ><!-- 仅显示前10个字符 -->
               <span >
                {{ row[item.prop].length > 10 ? row[item.prop].slice(0, 10) + "..." : row[item.prop] }}
              </span>
            </el-tooltip>
          </template>
        </el-table-column>

        <!-- 自定义 Sequence 列，显示前10个字符并作为超链接 -->
        <el-table-column
            v-else-if="item.prop === 'Sequence'"
            :key="item.prop"
            :width="item.width ? item.width : 125"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-link
                :underline="false"
                @click="goToGeneInformationPage(row)"
                style="color: #409EFF;"
            >
              <span>{{ row[item.prop].length > 10 ? row[item.prop].slice(0, 10) + "..." : row[item.prop] }}</span>

            </el-link>
          </template>
        </el-table-column>

        <!-- 自定义 Pro_clst80 列，显示为超链接 -->
        <el-table-column
            v-else-if="item.prop === 'Pro_clst80'"
            :key="item.prop"
            :width="item.width ? item.width : 120"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-link
                :underline="false"
                @click="searchByProClst80(row.Pro_clst80)"
                style="color: #409EFF;"
            >
              {{ row.Pro_clst80 }}
            </el-link>
          </template>
        </el-table-column>

                <!-- 自定义 AMP_clst 列，显示为超链接 -->
        <el-table-column
            v-else-if="item.prop === 'AMP_clst'"
            :key="item.prop"
            :width="item.width ? item.width : 120"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-link
                :underline="false"
                @click="searchByAMPClst(row.AMP_clst)"
                style="color: #409EFF;"
            >
              {{ row.AMP_clst }}
            </el-link>
          </template>
        </el-table-column>

        <!-- 默认显示的其他列 -->
        <el-table-column
            v-else
            :key="item.prop"
            :width="item.prop === 'AMPlen' || item.prop === 'Position' ? 110 : (item.width ? item.width : 150)"
            :prop="item.prop"
            :label="item.label"
            sortable
        />
      </template>
    </el-table>
    <el-pagination
        class="pager"
        background
        layout="prev, pager, next"
        size="small"
        :total="config.total_page"
        @current-change = "handleChange"
    />
  </div>
    <!-- 页脚 -->
    <el-footer class="footer">
      <p>Copyright © 2024 AMP-SEMiner authors All rights reserved. The portal open source code is available in <a href="https://github.com/JackKuo666/AMP-SEMiner-Portal" target="_blank" rel="noopener noreferrer" class="blue-link">this link</a>.</p>
  </el-footer>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted, reactive, nextTick, computed} from "vue";
import {ElMessage, ElMessageBox, ElInput, ElDropdown, ElDropdownMenu, ElDropdownItem} from "element-plus";


const tableData = ref([])
const sources = ref( [
        { value: 'ancient_human_gut', label: 'Ancient Human Gut' },
        { value: 'BGI_human_oral', label: 'BGI Human Oral' },
        { value: 'data_CGMR', label: 'Data CGMR' },
        { value: 'data_Hadza', label: 'Data Hadza' },
        { value: 'MGnify_cow_rumen', label: 'MGnify Cow Rumen' },
        { value: 'MGnify_fish_gut', label: 'MGnify Fish Gut' },
        { value: 'MGnify_human_gut', label: 'MGnify Human Gut' },
        { value: 'MGnify_human_oral', label: 'MGnify Human Oral' },
        { value: 'MGnify_pig_gut', label: 'MGnify Pig Gut' },
        { value: 'MGnify_zibrafish_fecal', label: 'MGnify Zibrafish Fecal' },
        { value: 'All', label: 'All' },
      ])

const {proxy} = getCurrentInstance()
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


const searchForm = reactive({
  source: 'All',
  amp: '',
  proClst80: '',
  ampClst: '',
  amplenmin: 1,
  amplenmax: 500,
})

const formRef = ref(null);

// Computed property to check if at least one field is filled
const isValidForm = computed(() => {
  return Object.values(searchForm).some(value => value !== '' && value !== null);
});

const suggestions = ref(['KKFGKAAN', 'ASIKDFFKKIGDSIKKLFEKIFKP']);

// 自动补全查询函数
const querySearch = (queryString, cb) => {
  if (!suggestions.value) return cb([]);

  const lowerCaseQuery = queryString.toLowerCase();
  const results = queryString
    ? suggestions.value.filter(item => item.toLowerCase().includes(lowerCaseQuery))
    : suggestions.value;
  
  cb(results);
};

// 处理选择项
const handleSelect = (item) => {
  console.log('Selected:', item);
  searchForm.amp = item; // 更新表单中的值
};
// Handle search button click
const onSearch = () => {
  ElMessage.success("Search submitted with data: " + JSON.stringify(searchForm));
  if (searchForm.source === 'All') {
    config.source = ''
  }else{
    config.source = searchForm.source
  }
  config.amplenmin = searchForm.amplenmin
  config.amplenmax = searchForm.amplenmax
  config.amp = searchForm.amp
  config.proClst80 = NaN
  getUserData()
};

// Reset form to initial state
const resetForm = () => {
  // 刷新页面
  window.location.reload();
};

// 跳转
import { useRouter } from 'vue-router';

const router = useRouter();

const goToGeneInformationPage = async (row) => {
  console.log("goToGeneInformationPage sent:", row)
  console.log("goToGeneInformationPage config", {tables : "human_gut_amps", source : row.Source, proID : row.ProID, position : row.Position})
    // 调用 API 获取数据
  const response = await proxy.$api.getAllAmpsData( {tables : "human_gut_amps", source : row.Source, proID : row.ProID, position : row.Position});
  console.log("goToGeneInformationPage response", response.data);
      // 处理 API 返回的数据
  if (response && response.data.length > 0) {
    row = response.data[0]
  }
  console.log("goToGeneInformationPage row", row)

  if (!row) return; // 确保 row 存在
  localStorage.setItem('oneGeneData', JSON.stringify(row)); // 存储 row 数据
  router.push({ name: 'GeneInformationPage' }); // 跳转到 GeneInformationPage
};

// 搜索所有 Pro_clst80 相同的数据
const searchByProClst80 = (proClst80) => {
  ElMessage.success(`Searching for Pro_clst80: ${proClst80}`);
  // 在这里添加实际的搜索逻辑
  searchForm.proClst80 = proClst80; // 将当前 Pro_clst80 设置为搜索条件
  config.proClst80 = proClst80
  getUserData(); // 调用数据获取函数
  // config.proClst80 = NaN
};

// 搜索所有 AMPClst 相同的数据
const searchByAMPClst = (AMPClst) => {
  ElMessage.success(`Searching for Pro_clst80: ${AMPClst}`);
  // 在这里添加实际的搜索逻辑
  searchForm.ampClst = AMPClst; // 将当前 AMPClst 设置为搜索条件
  config.ampClst = AMPClst
  getUserData(); // 调用数据获取函数
};

//其中total是数据总条数，page是当前的页数，
const config = reactive({
  tables: 'all_amp_protein_animal',
  proID: '',
  position: '',
  total_page: 100,
  records_per_page: 18,
  page: 1,
  source: '',
  amp: '',
  proClst80: NaN,
  ampClst: NaN,
  amplenmin: 1,
  amplenmax: 500,
  sortProp: '',
  sortOrder: ''
})

const handleChange = (page)=>{
  config.page = page
  getUserData()
}

const handleSortChange = (sort) => {
  console.log('Sort changed:', sort);
  const { prop, order } = sort; // 获取排序的列和方向
  config.sortProp = prop
  config.sortOrder =   order === 'ascending' ? 'asc' : 'desc'
  if (order) {
    // 根据排序的列和方向调用 API 获取数据
    getUserData();
  }
};

// 添加 loading 状态
const loading = ref(false);

const getUserData = async () => {
  try {
    loading.value = true; // 开始加载
    console.log("config", config);
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
  } finally {
    loading.value = false; // 停止加载
  }
};




onMounted(()=>{
  getUserData()
})
</script>


<style lang="less" scoped >
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


.user-header{
  margin-top: 20px;
  display: flex;
  justify-content: right;
  .demo-form-inline{
    text-align: center;
  }
}
.autocomplete-popper {
  max-height: 200px; /* 设置最大高度 */
  overflow-y: auto; /* 添加滚动条 */
  width: 100%; /* 确保宽度与输入框一致 */
}

.suggestion-item {
  padding: 8px;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f0f0f0;
}

.table{
  position: relative;
  height: 95%;
  .el-table{
    width: 100%;
    height: 95%;
  }
  .pager{
    position: absolute;
    right: 10px;
    bottom: auto;
  }
}
.select-clearn{
  display: flex;
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
</style>